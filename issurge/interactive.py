from .parser import Issue


def create_issue(words: str) -> Issue:
    issue, expects_description = Issue.parse(words)
    if expects_description:
        print(
            "Please enter a description for the issue (submit 2 empty lines to finish):"
        )
        description = ""
        next_empty_is_finish = False
        while True:
            line = input("> ")
            if line == "":
                if next_empty_is_finish:
                    break
                next_empty_is_finish = True
            else:
                next_empty_is_finish = False

            description += line + "\n"

        issue = Issue(**(issue._asdict() | {"description": description.strip()}))

    return issue
