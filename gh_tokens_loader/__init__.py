"""Top-level package for gh-tokens-loader."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("gh-tokens-loader")
except PackageNotFoundError:
    __version__ = "uninstalled"

__author__ = "Eva Maxfield Brown"
__email__ = "evamaxfieldbrown@gmail.com"

from .tokens import load_gh_tokens, GitHubTokensCycler

__all__ = ["__version__", "__author__", "__email__", "load_gh_tokens", "GitHubTokensCycler",]