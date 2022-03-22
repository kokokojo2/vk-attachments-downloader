import argparse


arg_parser = argparse.ArgumentParser(
    description='Downloads attachments of messages from your personal Vkontakte archive.'
)
arg_parser.add_argument(
    'name',
    type=str,
    help='the name or path to your archive (can be unarchived)'
)

arg_parser.add_argument(
    '-i',
    '--ids',
    type=str,
    nargs='+',
    default=[],
    help='particular chat ids to download attachments from (omit to download everything)'
)

arg_parser.add_argument(
    '-c',
    '--chats',
    type=str,
    nargs='+',
    default=[],
    help='particular chat names to download attachments from (omit to download everything)'
)

