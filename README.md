# issurge

![GitHub branch checks state](https://img.shields.io/github/checks-status/gwennlbh/issurge/main) [![Codecov](https://img.shields.io/codecov/c/github/gwennlbh/issurge)](https://app.codecov.io/gh/gwennlbh/issurge) [![PyPI - Version](https://img.shields.io/pypi/v/issurge)](https://pypi.org/project/issurge) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/issurge)

Deal with your client's feedback efficiently by creating a bunch of issues in bulk from a text file.

![demo](./demo.gif)

## Supported platforms

- Gitlab (including custom instances): requires [`glab`](https://gitlab.com/gitlab-org/cli#installation) to be installed
- Github: requires [`gh`](https://github.com/cli/cli#installation) to be installed

## Installation

### With Pip(x)

Issurge is distributed on [PyPI](https://pypi.org/project/issurge), so you can install it with `pipx` (recommended) or `pip`.

```
pipx install issurge
```

> [!TIP]
> You can also use [uv's `tool` subcommand](https://docs.astral.sh/uv/guides/tools/#installing-tools), it's just like `pipx` but wayyy faster.
>
> ```
> uv tool install issurge
> ```

### Arch Linux

Issurge is [on the AUR](https://aur.archlinux.org/packages/issurge/), so you can install it with your favorite AUR helper, such as [paru](https://aur.archlinux.org/packages/paru/):

```
paru -S issurge
```

## Usage

The command needs to be run inside of the git repository (this is used to detect if the repository uses github or gitlab)

```
issurge  [options] <file> [--] [<submitter-args>...]
issurge --help
```

- **&lt;submitter-args&gt;** contains arguments that will be passed as-is to every `glab` (or `gh`) command.

### Options

- **--dry-run:** Don't actually post the issues
- **--debug:** Print debug information

### Syntax

See [Syntax](./issurge/SYNTAX.md)

### One-shot mode

You can also create a single issue directly from the command line with `issurge new`.

If you end the line with `:`, issurge will prompt you for more lines.

```sh-session
$ issurge --debug new ~enhancement add an interactive \"one-shot\" mode @me:
Please enter a description for the issue (submit 2 empty lines to finish):
> Basically allow users to enter an issue fragment directly on the command line with a subcommand, and if it expects a description, prompt for it
>
>
Submitting add an interactive "one-shot"  (...) ~enhancement @me [...]
Running gh issue new -t "add an interactive \"one-shot\" mode" -b "Basically allow users to enter an issue fragment directly on the command line with a subcommand, and if it expects a description, prompt for it" -a @me -l enhancement
```
