import os
from core import get_attachments
from args import arg_parser


if __name__ == '__main__':
    args = arg_parser.parse_args()

    if not os.path.isdir(args.name):
        raise NotImplementedError('The script currently accepts only unarchived inputs.')

    messages_path = os.path.join(args.name, 'messages/')
    dir_names = os.listdir(messages_path) if not args.chats else args.chats

    folder_entries = map(lambda x: os.path.join(messages_path, x), dir_names)
    chat_dirs = list(filter(lambda x: os.path.isdir(x), folder_entries))

    print(f'Found {len(chat_dirs)} chats.')
    get_attachments(chat_dirs)
