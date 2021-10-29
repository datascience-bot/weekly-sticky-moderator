"""Run weekly sticky moderator."""
from argparse import ArgumentParser
from os import getenv
from typing import Dict

import boto3
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


def main(reddit: praw.models.Reddit):
    """Moderate submissions on r/datascience."""
    subreddit = reddit.subreddit("datascience")
    old_thread = get_last_thread(subreddit)
    new_thread = create_weekly_sticky(subreddit)
    remediate_comments(old_thread, new_thread)


def lambda_handler(event: Dict = None, context: Dict = None):
    """Handle AWS Lambda invocations.

    The `event` and `context` parameters are required by the AWS Lambda handler,
    but they are not used in the application.

    See also:
        https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html
    """
    client = boto3.client("ssm")
    param_names = {
        "client_id": getenv("SSM_PRAW_CLIENT_ID"),
        "client_secret": getenv("SSM_PRAW_CLIENT_SECRET"),
        "username": getenv("SSM_PRAW_USERNAME"),
        "password": getenv("SSM_PRAW_PASSWORD"),
    }
    kwargs = {
        k: client.get_parameter(p, WithDecryption=True)["Parameter"]["Value"]
        for k, p in param_names.items()
    }
    main(**kwargs)


if __name__ == "__main__":
    # Helpful for local development.
    flags = FLAGS.parse_args()
    reddit = praw.Reddit(
        client_id=flags.client_id,
        client_secret=flags.client_secret,
        username=flags.username,
        password=flags.password,
        user_agent="u/datascience-bot",
    )
    main(reddit)
