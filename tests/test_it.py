"""Test Weekly Sticky Moderator."""
from datetime import datetime
from unittest.mock import Mock

import pytest

from app import create_weekly_sticky
from app import get_last_thread
from app import InvalidConditionError
from app import remediate_comments


def test_create_weekly_sticky__attributes(subreddit):
    submission = create_weekly_sticky(subreddit, time=datetime(2021, 10, 31))

    submission.mod.approve.assert_called_once()
    submission.mod.distinguish.assert_called_once()
    submission.mod.flair.assert_called_once()
    submission.mod.sticky.assert_called_once()
    submission.mod.suggested_sort.assert_called_once()


def test_get_last_thread(subreddit):
    actual = get_last_thread(subreddit)

    sticky, submission = subreddit.hot()
    if sticky.author != "datascience-bot":
        submission, sticky = sticky, submission
    expected = sticky

    assert actual is expected


def test_get_last_thread__error(subreddit):
    subreddit = Mock()
    subreddit.hot.return_value = [Mock(), Mock()]
    with pytest.raises(InvalidConditionError):
        get_last_thread(subreddit)


def test_remediate_comments(weekly_thread):
    remediate_comments(weekly_thread, to_thread=Mock())

    for comment in weekly_thread.comments:
        if len(comment.replies) == 0:
            comment.reply.assert_called_once()
        else:
            comment.assert_not_called()
