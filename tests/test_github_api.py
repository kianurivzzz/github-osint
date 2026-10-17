from unittest.mock import Mock, patch

import requests

import github_api


def make_response(data):
    response = Mock()
    response.json.return_value = data
    response.raise_for_status.return_value = None
    return response


def make_commit(email):
    return {"commit": {"author": {"email": email}}}


@patch("github_api.requests.get")
def test_get_profile(mock_get):
    mock_get.return_value = make_response({
        "login": "octocat",
        "name": "The Octocat",
        "company": "@github",
        "location": "San Francisco",
        "blog": "https://github.blog",
        "created_at": "2011-01-25T18:44:36Z",
    })

    profile = github_api.get_profile("octocat", token=None)

    assert profile["name"] == "The Octocat"
    assert profile["location"] == "San Francisco"


@patch("github_api.requests.get")
def test_token_goes_to_header(mock_get):
    mock_get.return_value = make_response({"login": "octocat", "created_at": "2011-01-25T18:44:36Z"})

    github_api.get_profile("octocat", token="test-token")

    headers = mock_get.call_args.kwargs["headers"]
    assert headers["Authorization"] == "Bearer test-token"


@patch("github_api.requests.get")
def test_get_repos_skips_forks(mock_get):
    mock_get.return_value = make_response([
        {"name": "Hello-World", "fork": False},
        {"name": "Spoon-Knife", "fork": True},
    ])

    assert github_api.get_repos("octocat", token=None) == ["Hello-World"]


@patch("github_api.requests.get")
def test_get_commit_emails_skips_noreply(mock_get):
    mock_get.return_value = make_response([
        make_commit("octocat@example.com"),
        make_commit("583231+octocat@users.noreply.github.com"),
        make_commit("octocat@example.com"),
    ])

    emails = github_api.get_commit_emails("octocat", ["Hello-World"], token=None)

    assert emails == ["octocat@example.com"]


@patch("github_api.requests.get")
def test_get_commit_emails_skips_empty_repo(mock_get):
    error = Mock()
    error.raise_for_status.side_effect = requests.HTTPError("409 Client Error")
    mock_get.side_effect = [error, make_response([make_commit("octocat@example.com")])]

    emails = github_api.get_commit_emails("octocat", ["empty", "Hello-World"], token=None)

    assert emails == ["octocat@example.com"]
