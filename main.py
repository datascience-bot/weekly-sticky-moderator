"""Run weekly sticky moderator."""
from argparse import ArgumentParser
from os import getenv

import praw

from app import create_weekly_sticky
from app import get_last_thread
from app import remediate_comments


FLAGS = ArgumentParser()

FLAGS.add_argument(
    "-u",
    "--username",
    action="store",
    default=getenv("PRAW_USERNAME"),
    dest="username",
    required=False,
    type=str,
    help="Reddit user's username.",
)
FLAGS.add_argument(
    "-p",
    "--password",
    action="store",
    default=getenv("PRAW_PASSWORD"),
    dest="password",
    required=False,
    type=str,
    help="Reddit user's password.",
)
FLAGS.add_argument(
    "-c",
    "--client_id",
    action="store",
    default=getenv("PRAW_CLIENT_ID"),
    dest="client_id",
    required=False,
    type=str,
    help="Reddit API client_id.",
)
FLAGS.add_argument(
    "-s",
    "--client_secret",
    action="store",
    default=getenv("PRAW_CLIENT_SECRET"),
    dest="client_secret",
    required=False,
    type=str,
    help="Reddit API client_secret.",
)


def main():
    """Login to reddit and moderate submissions."""
    flags = FLAGS.parse_args()

    reddit = praw.Reddit(
        client_id=flags.client_id,
        client_secret=flags.client_secret,
        user_agent="u/datascience-bot",
        username=flags.username,
        password=flags.password,
    )

    subreddit = reddit.subreddit("datascience")
    old_thread = get_last_thread(subreddit)
    new_thread = create_weekly_sticky(subreddit)
    remediate_comments(old_thread, new_thread)


if __name__ == "__main__":
    main()
