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

Indentation is done with tab characters only.

- **Title:** The title is made up of any word in the line that does not start with `~`, `@`, `%` or `#.`. Words that start with any of these symbols will not be added to the title, except if they are in the middle (in that case, they both get added as tags/assignees/milestones and as a word in the title, without the prefix symbol)
- **Tags:** Prefix a word with `~` to add a label to the issue. For github repositories under an organization, if the label case-insensitively matches a defined issue type, the label will not be added, but the issue type will be set. Setting multiple issue types results in an error.
- **Assignees:** Prefix with `@` to add an assignee. The special assignee `@me` is supported.
- **Milestone:** Prefix with `%` to set the milestone
- **References:** Prefix with `#.NUMBER` to define a reference for this issue. See [Cross-reference other issues](#cross-reference-other-issues) for more information.
- **Comments:** You can add comments by prefixing a line with `//`
- **Description:** To add a description, finish the line with `:`, and put the description on another line (or multiple), just below, indented once more than the issue's line. Exemple:

  ```
  My superb issue ~some-tag:
       Here is a description

       I can skip lines
  Another issue
  ```

  Note that you cannot have indented lines inside of the description (they will be ignored).

#### Add some properties to multiple issues

You can apply something (a tag, a milestone, an assignee) to multiple issues by indenting them below:

```
One issue

~common-tag
    ~tag1 This issue will have tags:
        - tag1
        - common-tag
    @me this issue will only have common-tag as a tag.

Another issue.
```

#### Cross-reference other issues

As you might know, you can link an issue to another by using `#NUMBER`, with `NUMBER` the number of the issue you want to reference. You could want to write that, to reference `First issue` in `Second issue`:

```
First issue

Second issue:
  Needs #11
```

However, this assumes that the current latest issue, before running issurge on this file, is `#9`. It also assumes that issues get created in order (which is the case for now), and that no other issue will get created while running issurge.

As managing all of this by hand can be annoying, you can create references in the issurge file:

```
#.1 First issue

Second issue:
  Needs #.1
```

And that `#.1` in `Needs #.1` will be replaced by the actual issue number of `First issue` when the issue gets created.

> [!WARNING]
> For now, issues are created in order, so you need to define a reference _before_ you can use it.

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
