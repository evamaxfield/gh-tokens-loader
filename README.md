# GitHub Tokens Loader

A simple utility library to load GitHub tokens from a structured file which helps track who the token is linked to and when it expires.

## Usage

### GitHub Tokens File

To use this library, create a file with the following structure:

```yaml
tokens:
  eva:
    token: "github_pat_56..."
    expiration_date: null
  izzy:
    token: "github_pat_41..."
    expiration_date: "2026-02-13"
  soham:
    token: "ghp_VeaD3..."
    expiration_date: null
  isaac:
    token: "ghp_VVv5E..."
    expiration_date: "2023-02-13"
```

Each token has a short name (generally who or what it is linked to), the token itself, and an optional expiration date. The expiration date should be in the format `YYYY-MM-DD`.

⚠️⚠️ **Important:** Do not share this file with anyone else. Keep it secure and private. It is recommended to add the filename to your `.gitignore` as well. ⚠️⚠️

### Loading Tokens

To load the tokens from the file, use the following code:

```python
from github_tokens_loader import load_github_tokens

tokens = load_github_tokens("path/to/tokens.yaml")
```

This will return only the tokens that are valid (i.e., not expired).

## Why

I am a researcher who spends a lot of time mining the GitHub API for data about scientific software. Due to the rate limits on the GitHub API, other researchers in my department commonly share their tokens with me to help me get the data I need. I found myself copy pasting some form of this code around to different projects and decided to make it a library.

In my own usage, I generally use the GitHubTokensCycler that is also builtin to the library:

```python
import time
from concurrent.futures import ThreadPoolExecutor

from github_tokens_loader import GitHubTokensCycler

# Load tokens
gh_tokens_cycler = GitHubTokensCycler("path/to/tokens.yaml")

# Imagine some function that uses the GitHub API
def get_repo_data(repo: str, gh_token: str) -> dict:
    # Important to sleep to avoid rate limits
    time.sleep(1)

    # Use the token to get data from the GitHub API
    # ...
    # Return the data
    return {"some": "data"}

# Imagine some list of repos
repos = ["repo1", "repo2", "repo3", "..."]

# Thread with cycling tokens
with ThreadPoolExecutor(max_workers=len(gh_tokens_cycler)) as exe:
    results = list(exe.map(
        get_repo_data,
        repos,
        [next(gh_tokens_cycler) for _ in range(len(repos))],
    ))

# Do something with the results
# ...
```

The `GitHubTokensCycler` will occasionally also refresh it's internal set of tokens to only include valid tokens.

## License

This project is licensed under the Mozilla Public License 2.0 - see the [LICENSE](LICENSE) file for details.