# issurge

Deal with your client's feedback efficiently by creating a bunch of issues in bulk from a text file.

Only supports gitlab for now.

Requires `glab`.

## Installation

```
pip install issurge
```

## Usage

```
issurge  [options] <file> [--] [<glab-args>...]
issurge --help
```

- **<glab-args>** contains arguments that will be passed as-is to every `glab` command.

### Options

- **--dry-run:** Don't actually post the issues
- **--debug:** Print debug information

### Syntax

Indentation is done with tab characters only.

- **Title:** The title is made up of any word in the line that does not start with `~`, `@` or `%`.
- **Tags:** Prefix a word with `~` to add a label to the issue
- **Assignees:** Prefix with `@` to add an assignee. The special assignee `@me` is supported.
- **Milestone:** Prefix with `%` to set the milestone
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


