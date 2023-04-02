# issurge

![GitHub branch checks state](https://img.shields.io/github/checks-status/ewen-lbh/issurge/main) ![Codecov](https://img.shields.io/codecov/c/github/ewen-lbh/issurge)

Deal with your client's feedback efficiently by creating a bunch of issues in bulk from a text file.

## Supported platforms

- Gitlab (including custom instances): requires [`glab`](https://gitlab.com/gitlab-org/cli#installation) to be installed
- Github: requires [`gh`](https://github.com/cli/cli#installation) to be installed

## Installation

```
pip install issurge
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

- **Title:** The title is made up of any word in the line that does not start with `~`, `@` or `%`. Words that start with any of these symbols will not be added to the title, except if they are in the middle (in that case, they both get added as tags/assignees/milestones and as a word in the title, without the prefix symbol)
- **Tags:** Prefix a word with `~` to add a label to the issue
- **Assignees:** Prefix with `@` to add an assignee. The special assignee `@me` is supported.
- **Milestone:** Prefix with `%` to set the milestone
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
