#!/usr/bin/env python

from gh_tokens_loader import load_gh_tokens, GitHubTokensCycler
import pytest

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