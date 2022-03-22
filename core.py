import requests
import os
import imghdr
import codecs
from bs4 import BeautifulSoup
from urllib import parse
from halo import Halo


def get_contents_bs4(filename):
    with codecs.open(filename, 'rb') as f:
        return BeautifulSoup(f, 'lxml')


def save_contents_bs4(filename, bs4_obj):
    with open(filename, 'w') as f:
        f.write(str(bs4_obj))


def parse_media_links(bs4_chat):
    raw_links = bs4_chat.find_all('a', {'class': 'attachment__link'})
    return list(map(lambda x: x.get('href').replace('amp;', ''), raw_links))


def clean_url(url):
    return url.replace('amp;', '')


def get_media_links(bs4_chat, only_public=False):
    links = bs4_chat.find_all('a', {'class': 'attachment__link'})
    if only_public:
        links = filter(lambda x: x.get('href').find('.userapi.com') != -1, links)

    yield from links


def get_chat_name(chat_id, root_path):
    soup = get_contents_bs4(os.path.join(root_path, 'index-messages.html'))
    return soup.find('a', {'href': f'{chat_id}/messages0.html'}).text


def get_filename_from_url(url):
    return parse.urlparse(url).path.split('/')[-1]


def get_attachment(url, filepath='', filename=None):
    full_path = os.path.join(filepath, get_filename_from_url(url) if not filename else filename)

    response = requests.get(url, allow_redirects=True)
    if response.status_code == 200:
        with open(full_path, 'wb') as f:
            f.write(response.content)

        return full_path


def get_chat_attachments(chat_path, save_path=None):
    if not save_path:
        save_path = chat_path

    if not os.path.exists(save_path):
        raise ValueError(f'Specified path({save_path}) does not exist.')

    if not os.path.exists(chat_path):
        raise ValueError(f'Specified path({chat_path}) does not exist.')

    base_message = \
        f'Downloading attachments for "{get_chat_name(os.path.basename(chat_path), os.path.dirname(chat_path))}"'
    attachment_counter = 0
    spinner = Halo(text=base_message, spinner='dots')
    spinner.start()

    for file in os.listdir(chat_path):
        if file.endswith('.html'):
            file_path = os.path.join(chat_path, file)
            messages_soup = get_contents_bs4(file_path)

            for link in get_media_links(messages_soup, only_public=True):
                attachment_path = get_attachment(clean_url(link['href']), filepath=save_path)
                append_attachment_local(messages_soup, link, attachment_path)

                attachment_counter += 1
                spinner.text = base_message + f' | {attachment_counter} {"items" if attachment_counter != 1 else "item"}'

            save_contents_bs4(file_path, messages_soup)

    spinner.succeed()


def append_attachment_local(soup_obj, attachment_div, attachment_path):
    attachment_view_element = None
    src_path = os.path.join('attachments/', os.path.basename(attachment_path))
    if imghdr.what(attachment_path):
        attachment_view_element = soup_obj.new_tag('img')
        attachment_view_element['src'] = src_path

    if attachment_path.endswith('.ogg') or attachment_path.endswith('.mp3'):
        attachment_view_element = soup_obj.new_tag('audio')
        attachment_view_element['controls'] = None

        audio_source = soup_obj.new_tag('source')
        audio_source['src'] = src_path
        audio_source['type'] = 'audio/' + attachment_path.split('.')[-1]
        attachment_view_element.append(audio_source)

    attachment_div.parent.append(attachment_view_element)


def get_attachments(dirs):
    for chat_path in dirs:
        save_path = os.path.join(chat_path, 'attachments/')

        try:
            os.mkdir(save_path)
        except FileExistsError:
            pass

        get_chat_attachments(chat_path, save_path)

