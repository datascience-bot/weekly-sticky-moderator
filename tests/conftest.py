"""Configure tests."""
from unittest.mock import Mock

import pytest

from app import TITLE_PREFIX


@pytest.fixture(scope="function")
def subreddit():
    """Mock a subreddit with the commonly accessed attributes."""
    sticky = Mock()
    sticky.title = TITLE_PREFIX
    sticky.stickied = True
    sticky.author = "datascience-bot"

    submission = Mock()
    submission.stickied = True

    subreddit = Mock()
    subreddit.hot.return_value = [submission, sticky]
    subreddit.submit.return_value = Mock()

    return subreddit


@pytest.fixture(scope="function")
def weekly_thread():
    """Mock a weekly thread with the commonly accessed attributes."""
    submission = Mock()
    unanswered_comment = Mock()
    unanswered_comment.replies = []
    answered_comment = Mock()
    answered_comment.replies = [Mock(), Mock(), Mock()]
    submission.comments = [answered_comment, unanswered_comment]

    return submission
