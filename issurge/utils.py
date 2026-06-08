import os
import subprocess

from rich import print


def debugging():
    return os.environ.get("ISSURGE_DEBUG")


def dry_running():
    return os.environ.get("ISSURGE_DRY_RUN")


def debug(*args, **kwargs):
    if os.environ.get("ISSURGE_DEBUG"):
        print(*args, **kwargs)


def run(command, bypass_dry_run=False):
    if dry_running() or debugging():
        print(
            f"{'Would run' if dry_running() and not bypass_dry_run else 'Running'} [white bold]{subprocess.list2cmdline(command)}[/]"
        )
    if not dry_running() or bypass_dry_run:
        try:
            out = subprocess.run(command, check=True, capture_output=True)
            return out.stderr.decode() + "\n" + out.stdout.decode()
        except subprocess.CalledProcessError as e:
            print(
                f"Calling [white bold]{e.cmd}[/] failed with code [white bold]{e.returncode}[/]:\n{NEWLINE.join(TAB + line for line in e.stderr.decode().splitlines())}"
            )


TAB = "\t"
NEWLINE = "\n"
