from unittest.mock import Mock, patch

import telegram_bot

PROFILE = {
    "login": "octocat",
    "name": "The Octocat",
    "company": None,
    "location": "San Francisco",
    "blog": "",
    "created_at": "2011-01-25T18:44:36Z",
}


def test_build_report():
    report = telegram_bot.build_report(PROFILE, ["Hello-World"], ["octocat@example.com"])

    assert "GitHub: octocat" in report
    assert "Город: San Francisco" in report
    assert "Компания" not in report
    assert "Аккаунт создан: 2011-01-25" in report
    assert "octocat@example.com" in report


def test_build_report_without_emails():
    report = telegram_bot.build_report(PROFILE, [], [])

    assert "Почта из коммитов не найдена" in report


@patch("telegram_bot.requests.post")
def test_send_message(mock_post):
    mock_post.return_value = Mock()

    telegram_bot.send_message("Привет", token="123:abc", chat_id="42")

    url = mock_post.call_args.args[0]
    payload = mock_post.call_args.kwargs["json"]
    assert url == "https://api.telegram.org/bot123:abc/sendMessage"
    assert payload == {"chat_id": "42", "text": "Привет"}
