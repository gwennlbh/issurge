#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "ruamel.yaml",
#   "tomlkit",
# ]
# ///

"""Synchronize Python support metadata and GitHub Actions workflows."""

from __future__ import annotations

import re
from pathlib import Path

import tomlkit
from ruamel.yaml import YAML

ROOT = Path(__file__).resolve().parents[1]
PYPROJECT = ROOT / "pyproject.toml"
CI = ROOT / ".github/workflows/ci.yml"
PR = ROOT / ".github/workflows/pr.yml"
RELEASE = ROOT / ".github/workflows/release.yml"

yaml = YAML()
yaml.preserve_quotes = True
yaml.indent(mapping=2, sequence=4, offset=2)
yaml.width = 4096


def load_yaml(path: Path):
    with path.open(encoding="utf-8") as file:
        data = yaml.load(file)

    if not isinstance(data, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain a YAML mapping")

    return data


def save_yaml(path: Path, data) -> None:
    with path.open("w", encoding="utf-8") as file:
        yaml.dump(data, file)


def get_job(workflow, name: str, path: Path):
    try:
        job = workflow["jobs"][name]
    except (KeyError, TypeError) as exc:
        raise ValueError(f"Expected job {name!r} in {path.relative_to(ROOT)}") from exc

    if not isinstance(job, dict):
        raise ValueError(f"Job {name!r} must be a mapping")

    return job


def get_python_version(value: str) -> tuple[int, int, int]:
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", str(value))

    if not match:
        raise ValueError(f"Expected a pinned Python X.Y.Z version, got {value!r}")

    version = tuple(map(int, match.groups()))

    if version[0] != 3:
        raise ValueError(f"Expected Python 3.x, got {value!r}")

    return version


def update_python_matrix(
    job,
    versions: list[str],
    latest: str,
    *,
    include_latest: bool,
) -> None:
    matrix = job.setdefault("strategy", {}).setdefault("matrix", {})

    print(f"Updating matrix for job {job.get('name', '<unnamed>')} to {versions}")

    if include_latest:
        matrix.pop("python-version", None)
        matrix.pop("is-latest", None)

        matrix["include"] = [
            {
                "python-version": version,
                "is-latest": version == latest,
            }
            for version in versions
        ]
    else:
        matrix["python-version"] = versions


def update_pinned_python(job, version: str, path: Path) -> None:
    steps = job.get("steps", [])

    matches = [
        step
        for step in steps
        if isinstance(step, dict)
        and str(step.get("uses", "")).startswith("actions/setup-python@")
    ]

    if len(matches) != 1:
        raise ValueError(
            f"Expected exactly one setup-python step in "
            f"{path.relative_to(ROOT)}, found {len(matches)}"
        )

    step = matches[0]
    inputs = step.setdefault("with", {})
    inputs["python-version"] = version


def update_project_metadata(target_major: int, target_minor: int) -> None:
    with PYPROJECT.open(encoding="utf-8") as file:
        project = tomlkit.load(file)

    metadata = project["project"]
    minimum = target_minor - 2
    metadata["requires-python"] = f">={target_major}.{minimum}"

    classifiers = metadata["classifiers"]

    # Preserve unrelated classifiers and remove obsolete Python minor versions.
    retained = [
        item
        for item in classifiers
        if not str(item).startswith("Programming Language :: Python :: ")
    ]

    classifiers = [*retained, "Programming Language :: Python :: 3 :: Only"]

    for minor in range(minimum, target_minor + 1):
        print(f"Adding Python {target_major}.{minor} classifier")
        classifiers.append(f"Programming Language :: Python :: {target_major}.{minor}")

    # Dedupe
    classifiers = list(dict.fromkeys(classifiers))

    metadata["classifiers"] = classifiers

    with PYPROJECT.open("w", encoding="utf-8") as file:
        tomlkit.dump(project, file)


def main() -> None:
    ci = load_yaml(CI)
    pr = load_yaml(PR)
    release = load_yaml(RELEASE)

    upload_job = get_job(ci, "upload-package", CI)

    pinned_step = next(
        (
            step
            for step in upload_job.get("steps", [])
            if isinstance(step, dict)
            and str(step.get("uses", "")).startswith("actions/setup-python@")
        ),
        None,
    )

    if pinned_step is None:
        raise ValueError("No setup-python step found in ci.yml upload-package job")

    raw_version = pinned_step.get("with", {}).get("python-version", "")
    target_major, target_minor, target_patch = get_python_version(raw_version)

    if target_minor < 15:
        raise ValueError(
            f"Unexpected Python migration target: "
            f"{target_major}.{target_minor}.{target_patch}"
        )

    target = f"{target_major}.{target_minor}"
    minimum = target_minor - 3

    update_project_metadata(target_major, target_minor)

    ci_job = get_job(ci, "test", CI)
    ci_versions = [
        f"{target_major}.{minor}" for minor in range(minimum, target_minor + 1)
    ]

    update_python_matrix(
        ci_job,
        ci_versions,
        target,
        include_latest=True,
    )

    release_job = get_job(release, "release", RELEASE)
    update_pinned_python(release_job, str(raw_version), RELEASE)

    pr_job = get_job(pr, "test", PR)
    pr_versions = [
        f"{target_major}.{minor}" for minor in range(minimum, target_minor + 1)
    ]

    update_python_matrix(
        pr_job,
        pr_versions,
        target,
        include_latest=False,
    )

    save_yaml(CI, ci)
    save_yaml(PR, pr)
    save_yaml(RELEASE, release)


if __name__ == "__main__":
    main()
