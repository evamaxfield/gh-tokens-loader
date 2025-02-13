#!/usr/bin/env python

import time
from concurrent.futures import ThreadPoolExecutor

import pytest

from gh_tokens_loader import GitHubTokensCycler, load_gh_tokens

from .conftest import EXAMPLE_GH_TOKENS_FILE

###############################################################################

# As much as I would love to test with freezegun for datetime mocking,
# it is hard to manage due to the msgspec struct having datetime parsing from strings

###############################################################################


def test_load_gh_tokens_default() -> None:
    """Test load_gh_tokens with default arguments."""
    gh_tokens = load_gh_tokens(EXAMPLE_GH_TOKENS_FILE)
    assert len(gh_tokens) == 4
    assert gh_tokens == {
        "github_pat_56...",
        "github_pat_41...",
        "ghp_VeaD3...",
        "ghp_efghi...",
    }


def test_load_gh_tokens_all() -> None:
    """Test load_gh_tokens with all tokens."""
    gh_tokens = load_gh_tokens(EXAMPLE_GH_TOKENS_FILE, return_all=True)
    assert len(gh_tokens) == 6
    assert gh_tokens == {
        "github_pat_56...",
        "github_pat_41...",
        "ghp_VeaD3...",
        "ghp_VVv5E...",
        "ghp_abcde...",
        "ghp_efghi...",
    }


def test_load_gh_tokens_strict_dates() -> None:
    """Test load_gh_tokens with strict date parsing."""
    with pytest.raises(ValueError, match="Error parsing date"):
        load_gh_tokens(EXAMPLE_GH_TOKENS_FILE, strict_date_parsing=True)


def test_tokens_cycler() -> None:
    """Test GitHubTokensCycler."""
    cycler = GitHubTokensCycler(EXAMPLE_GH_TOKENS_FILE)

    # Should loop after 4
    seen_tokens = set()
    for token in cycler:
        if token in seen_tokens:
            break
        seen_tokens.add(token)

    assert len(seen_tokens) == 4


def test_tokens_cycler_refresh() -> None:
    """Test GitHubTokensCycler refresh."""
    cycler = GitHubTokensCycler(EXAMPLE_GH_TOKENS_FILE, refresh_every_n=2)

    # First cycle of two
    first_cycle = {next(cycler) for _ in range(2)}

    # Second cycle of two
    second_cycle = {next(cycler) for _ in range(2)}

    assert first_cycle == second_cycle


def smoke_test_readme_example() -> None:
    # Load tokens
    gh_tokens_cycler = GitHubTokensCycler("path/to/tokens.yaml")

    # Imagine some function that uses the GitHub API
    def get_repo_data(repo: str, gh_token: str) -> dict:
        # Important to sleep to avoid rate limits
        time.sleep(1)

        # Use the token to get data from the GitHub API
        # ...
        # Return the data
        return {"repo": repo, "token": gh_token}

    # Imagine some list of repos
    repos = ["repo1", "repo2", "repo3", "..."]

    # Thread with cycling tokens
    with ThreadPoolExecutor(max_workers=len(gh_tokens_cycler)) as exe:
        results = list(
            exe.map(
                get_repo_data,
                repos,
                [next(gh_tokens_cycler) for _ in range(len(repos))],
            )
        )

    # Assert that we have 4 results
    assert len(results) == 4

    # Assert that all tokens were used
    assert len({result["token"] for result in results}) == 4
