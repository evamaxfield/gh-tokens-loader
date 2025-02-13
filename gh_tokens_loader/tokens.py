#!/usr/bin/env python

from itertools import cycle

import os
from pathlib import Path
from datetime import datetime

import msgspec

from .types import MultipleTokenDetails

###############################################################################

def load_gh_tokens(
    gh_tokens_file: os.PathLike | str | Path = ".github-tokens.yaml",
    return_all: bool = False,
    strict_date_parsing: bool = False,
    report_expired: bool = True,
) -> set[str]:
    """
    Load GitHub Tokens from file.

    Parameters
    ----------
    gh_tokens_file : os.PathLike | str | Path, optional
        Path to the YAML file containing GitHub Tokens, by default ".github-tokens.yaml"
    return_all : bool, optional
        Return all tokens, by default False (only return non-expired tokens)
    strict_date_parsing : bool, optional
        Use strict date parsing, by default False (skip token if expiration date would raise an error)
    report_expired : bool, optional
        Report how many tokens are expired, by default True

    Returns
    -------
    set[str]
        Set of GitHub Tokens
    """
    # Open, read bytes, and parse
    with open(gh_tokens_file, "rb") as open_file:
        all_token_details = msgspec.yaml.decode(
            open_file.read(),
            type=MultipleTokenDetails,
        )

    # Get current date
    current_date = datetime.now()

    # Iter tokens and keep valid
    valid_tokens = set()
    n_expired = 0
    for short_name, details in all_token_details.tokens.items():
        # Handle fast route
        if return_all:
            valid_tokens.add(details.token)
            continue

        # Otherwise, check expiration
        if details.expiration_date is None:
            valid_tokens.add(details.token)
        else:
            # Try to parse date
            try:
                expiration_date = datetime.fromisoformat(details.expiration_date)
            except Exception as e:
                if strict_date_parsing:
                    raise ValueError(
                        f"Error parsing date ('{details.expiration_date}') "
                        f"for token details named: '{short_name}'"
                    ) from e
                continue

            # Add if not expired
            if expiration_date > current_date:
                valid_tokens.add(details.token)
            else:
                n_expired += 1

    # Report expired tokens
    if report_expired:
        print(f"Expired GitHub Tokens: {n_expired}")

    return valid_tokens


class GitHubTokensCycler:
    """
    Auto-refreshing tokens cycler.

    Parameters
    ----------
    gh_tokens_file : os.PathLike | str | Path, optional
        Path to the YAML file containing GitHub Tokens, by default ".github-tokens.yaml"
    refresh_every_n : int, optional
        Refresh tokens every n cycles, by default 1024
    kwargs: dict[str, bool]
        Extra keyword arguments to pass to load_gh_tokens
    """
    def __init__(
        self: "GitHubTokensCycler",
        gh_tokens_file: os.PathLike | str | Path = ".github-tokens.yaml",
        refresh_every_n: int = 1024,
        **kwargs: dict[str, bool],
    ):
        # Load tokens
        self._gh_tokens_file = gh_tokens_file
        self._extra_kwargs = kwargs
        self._load_tokens()

        # Store refresh every
        self._refresh_every_n = refresh_every_n

    def _load_tokens(self) -> None:
        self._gh_tokens = load_gh_tokens(self._gh_tokens_file, **self._extra_kwargs)
        self._cycled_tokens = cycle(self._gh_tokens)
        self._counter = 0

    def __len__(self) -> int:
        return len(self._gh_tokens)
    
    def _get_next_token(self) -> str:
        if self._counter % self._refresh_every_n == 0:
            self._load_tokens()
        
        # Increment counter
        self._counter += 1
        return next(self._cycled_tokens)

    def __next__(self):
        return self._get_next_token()
    
    def __iter__(self):
        return self