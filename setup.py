# -*- coding: utf-8 -*-
from setuptools import setup

packages = ["issurge"]

package_data = {"": ["*"]}

install_requires = ["docopt>=0.6.2,<0.7.0", "rich>=13.3.3,<14.0.0"]

entry_points = {"console_scripts": ["issurge = issurge.main:run"]}

setup_kwargs = {
    "name": "issurge",
    "version": "0.4.0",
    "description": "Deal with your client's feedback efficiently by creating a bunch of issues in bulk from a text file.",
    "long_description": '# issurge\n\n![GitHub branch checks state](https://img.shields.io/github/checks-status/ewen-lbh/issurge/main) ![Codecov](https://img.shields.io/codecov/c/github/ewen-lbh/issurge)\n\nDeal with your client\'s feedback efficiently by creating a bunch of issues in bulk from a text file.\n\n## Supported platforms\n\n- Gitlab (including custom instances): requires [`glab`](https://gitlab.com/gitlab-org/cli#installation) to be installed\n- Github: requires [`gh`](https://github.com/cli/cli#installation) to be installed\n\n## Installation\n\n```\npip install issurge\n```\n\n## Usage\n\nThe command needs to be run inside of the git repository (this is used to detect if the repository uses github or gitlab)\n\n```\nissurge  [options] <file> [--] [<submitter-args>...]\nissurge --help\n```\n\n- **&lt;submitter-args&gt;** contains arguments that will be passed as-is to every `glab` (or `gh`) command.\n\n### Options\n\n- **--dry-run:** Don\'t actually post the issues\n- **--debug:** Print debug information\n\n### Syntax\n\nIndentation is done with tab characters only.\n\n- **Title:** The title is made up of any word in the line that does not start with `~`, `@` or `%`. Words that start with any of these symbols will not be added to the title, except if they are in the middle (in that case, they both get added as tags/assignees/milestones and as a word in the title, without the prefix symbol)\n- **Tags:** Prefix a word with `~` to add a label to the issue\n- **Assignees:** Prefix with `@` to add an assignee. The special assignee `@me` is supported.\n- **Milestone:** Prefix with `%` to set the milestone\n- **Comments:** You can add comments by prefixing a line with `//`\n- **Description:** To add a description, finish the line with `:`, and put the description on another line (or multiple), just below, indented once more than the issue\'s line. Exemple:\n\n  ```\n  My superb issue ~some-tag:\n       Here is a description\n\n       I can skip lines\n  Another issue\n  ```\n\n  Note that you cannot have indented lines inside of the description (they will be ignored).\n\n#### Add some properties to multiple issues\n\nYou can apply something (a tag, a milestone, an assignee) to multiple issues by indenting them below:\n\n```\nOne issue\n\n~common-tag\n    ~tag1 This issue will have tags:\n        - tag1\n        - common-tag\n    @me this issue will only have common-tag as a tag.\n\nAnother issue.\n```\n\n### One-shot mode\n\nYou can also create a single issue directly from the command line with `issurge new`.\n\nIf you end the line with `:`, issurge will prompt you for more lines.\n\n```sh-session\n$ issurge --debug new ~enhancement add an interactive \\"one-shot\\" mode @me:\nPlease enter a description for the issue (submit 2 empty lines to finish):\n> Basically allow users to enter an issue fragment directly on the command line with a subcommand, and if it expects a description, prompt for it\n> \n> \nSubmitting add an interactive "one-shot"  (...) ~enhancement @me [...]\nRunning gh issue new -t "add an interactive \\"one-shot\\" mode" -b "Basically allow users to enter an issue fragment directly on the command line with a subcommand, and if it expects a description, prompt for it" -a @me -l enhancement\n```\n',
    "author": "Ewen Le Bihan",
    "author_email": "hey@ewen.works",
    "maintainer": "None",
    "maintainer_email": "None",
    "url": "https://github.com/ewen-lbh/issurge",
    "packages": packages,
    "package_data": package_data,
    "install_requires": install_requires,
    "entry_points": entry_points,
    "python_requires": ">=3.10,<4.0",
}


setup(**setup_kwargs)
