from rich import print
import os


def debug(*args, **kwargs):
    if os.environ.get("ISSURGE_DEBUG"):
        print(*args, **kwargs)


TAB = "\t"
