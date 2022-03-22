import os
from core import get_attachments, get_chat_id, get_or_rise_exc
from args import arg_parser


if __name__ == '__main__':
    args = arg_parser.parse_args()

    if not os.path.isdir(args.name):
        raise NotImplementedError('The script currently accepts only unarchived inputs.')

    messages_path = os.path.join(args.name, 'messages/')

    dir_args = {get_chat_id(chat_name, messages_path) for chat_name in args.chats}
    dir_args.update(set(args.ids))

    dir_names = os.listdir(messages_path) if not dir_args else dir_args

    folder_entries = map(lambda x: os.path.join(messages_path, x), dir_names)
    chat_dirs = list(filter(
        lambda x: get_or_rise_exc(x, os.path.isdir, f'Chat with id {os.path.basename(x)} not found.'),
        folder_entries
    ))

    print(f'Found {len(chat_dirs)} chats.')
    get_attachments(chat_dirs)
