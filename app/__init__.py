"""Maintain weekly Entering & Transitioning thread.

1. Author the new thread.
2. Redirect questions with no answers to the new thread.
3. Do 1 and 2 exactly once on Sundays.
"""
from datetime import datetime
from datetime import timedelta

import praw

TITLE_PREFIX: str = "Weekly Entering & Transitioning Thread"


class InvalidConditionError(Exception):
    """Raise errors on invalid conditions."""


def create_weekly_sticky(
    subreddit: praw.models.Subreddit, time: datetime = datetime.utcnow()
) -> praw.models.Submission:
    """Create a new Entering & Transitioning thread."""
    date_format = "%d %b %Y"
    start_date = time.strftime(date_format)
    end_date = (time + timedelta(days=7)).strftime(date_format)
    title = f"{TITLE_PREFIX} | {start_date} - {end_date}"

    with open("app/data/selftext.md") as ifile:
        selftext = ifile.read()

    submission = subreddit.submit(title, selftext, send_replies=False)
    submission.mod.approve()
    submission.mod.distinguish()
    submission.mod.flair(text="Discussion")
    submission.mod.sticky(state=True, bottom=True)
    submission.mod.suggested_sort(sort="new")

    return submission


def get_last_thread(subreddit: praw.models.Subreddit) -> praw.models.Submission:
    """Get the last weekly sticky thread."""
    for submission in subreddit.hot(limit=2):  # max 2 possible stickies
        if (
            submission.title.startswith(TITLE_PREFIX)
            and submission.stickied is True
            and submission.author == "datascience-bot"
        ):
            return submission
    else:
        raise InvalidConditionError("Could not find the last stickied thread.")


def remediate_comments(
    on_thread: praw.models.Submission, to_thread: praw.models.Submission
):
    """Direct unanswered comments to the new weekly sticky thread."""
    for comment in on_thread.comments:
        if len(comment.replies) > 0:
            continue

        msg = (
            f"Hi u/{comment.author}, I created a "
            f"[new Entering & Transitioning thread]({to_thread.permalink}). "
            "Since you haven't received any replies yet, "
            "please feel free to resubmit your comment in the new thread."
        )
        reply = comment.reply(msg)
        reply.mod.distinguish(how="yes")
