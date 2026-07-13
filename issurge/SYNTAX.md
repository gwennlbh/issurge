Indentation is done with tab characters only.

<!-- cli-help -->
- **Title:** The title is made up of any word in the line that does not start with `~`, `@`, `%`, `^`, `:` or `#.`. Words that start with any of these symbols will not be added to the title, except if they are in the middle (in that case, they both get added as tags/assignees/milestones and as a word in the title, without the prefix symbol)
- **Tags/Type:** Prefix a word with `~` to add a label to the issue. For github repositories under an organization, if the label case-insensitively matches a defined issue type, the label will not be added, but the issue type will be set. Setting multiple issue types results in an error.
- **Assignees:** Prefix with `@` to add an assignee. The special assignee `@me` is supported.
- **Milestone:** Prefix with `%` to set the milestone
- **References:** Prefix with `#.NUMBER` to define a reference for this issue. See [Cross-reference other issues](#cross-reference-other-issues) for more information.
- **Parent:** Prefix with `^` to set the parent of the issue we're creating to another issue. Use `^NUMBER` to set the parent to an already existing issue, or `^.REFERENCE` to set the parent thru a reference.
- **Blocked-by**: You can mark other issue(s) as blocking the issue you're creating by using `>NUMBER` or `>.REFERENCE` syntax (use `.REFERENCE` to set the dependency thru a reference). This works in the description as well, and (in the description only) the `>` will be replaced with a `#`, so that the issue gets linked to the blocking issue.
- **Comments:** You can add comments by prefixing a line with `//`
- **Description:** To add a description, finish the line with `:`, and put the description on another line (or multiple), just below, indented once more than the issue's line. Exemple:
- **Issue fields:** To set an issue field, use `:FIELD=VALUE`. For example, `thing :Area=App` will set the `Area` issue field to `App`.  If you have a single-select ("enum") field with all of its options being unambiguous (not clashing with any other option from any other single-select field of the org), you can shorten the syntax to `:VALUE`. Both field names and option names are case-insensitive, so you can avoid having to enter uppercase letters.
<!-- /cli-help -->

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

You can also use references to set the parent of an issue or a blocking dependency:

```
#.1 First issue

^.1 Sub-issue of the first issue

This one is not a sub-issue but:
  It will not work without it (see >.1)
```

> [!WARNING]
> For now, issues are created in order, so you need to define a reference _before_ you can use it.
