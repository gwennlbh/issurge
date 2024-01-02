from rich import print
import os


def debugging():
    return os.environ.get("ISSURGE_DEBUG")


def dry_running():
    return os.environ.get("ISSURGE_DRY_RUN")


def debug(*args, **kwargs):
    if os.environ.get("ISSURGE_DEBUG"):
        print(*args, **kwargs)


TAB = "\t"
NEWLINE = "\n"
