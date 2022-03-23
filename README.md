# VK-archive attachments downloader
This script downloads attachments for your Vkontakte archive backup.
You can get your archive that preserves all personal data including chat history, profile information, friends etc. [here](https://vk.com/data_protection?section=rules&scroll_to_archive=1).
However, this archive includes only links to mediafiles that are present in a chat history. The script can download all the media to store it localy on your computer.
## Usage

Clone the repo:

`git clone https://github.com/kokokojo2/vk-attachments-downloader`

`cd vk-attachments-downloader`

Install requirements:

`pip install -r requirements.txt`

Make sure to unpack your archive before usage.

Basic usage:

`python downloader.py path/to/your/arhive`

You can also specify the chat names or ids to download only their attachments:

`python downloader.py path/to/your/arhive --ids -1231443 200043243 --chats "My nice chat" "Doir Jhon"`
