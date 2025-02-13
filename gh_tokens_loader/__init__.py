"""Top-level package for gh-tokens-loader."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("gh-tokens-loader")
except PackageNotFoundError:
    __version__ = "uninstalled"

__author__ = "Eva Maxfield Brown"
__email__ = "evamaxfieldbrown@gmail.com"

from .tokens import GitHubTokensCycler, load_gh_tokens

__all__ = [
    "GitHubTokensCycler",
    "__author__",
    "__email__",
    "__version__",
    "load_gh_tokens",
]
