# -*- coding: utf-8 -*-
import re


def set_filename_version(filename, version_number, pattern):
    """Write the given version number in the given (in filename) file,
    after the given pattern.

    E.g.:
        set_filename_version('setup.py', '1.0.0', 'version')

    Extracted from Flask source, see:
        - file: flask/scripts/make-release.py
        - commit: 54688b26a9562c9a9c31541dbf32e0d8ee7a5926

    """
    def inject_version(match):
        before, old, after = match.groups()
        return before + version_number + after

    with open(filename) as f:
        contents = re.sub(r"^(\s*%s\s*=\s*')(.+?)(')(?sm)" % pattern,
                          inject_version, f.read())

    with open(filename, 'w') as f:
        f.write(contents)


def compute_semver(current_version, release='normal', compute_dev=True):
    """Compute and return the next version number, given a the current
    version and the release type ('normal', 'minor' or 'major'), as well
    as the next dev version (if `compute_dev` is 'True').

    """
    if current_version.endswith('dev'):
        dev_version = current_version.replace('dev', '')
        dev_version_parts = list(map(int, dev_version.split('.')))
        current_version_parts = dev_version_parts
        current_version_parts[2] -= 1
    else:
        current_version_parts = list(map(int, current_version.split('.')))

    release_version_parts = current_version_parts
    if release == 'minor':
        release_version_parts[2] += 1
    elif release == 'normal':
        release_version_parts[1] += 1
        release_version_parts[2] = 0
    elif release == 'major':
        release_version_parts[0] += 1
        release_version_parts[1] = 0
        release_version_parts[2] = 0

    release_version = '.'.join(map(str, release_version_parts))

    next_dev_version = None
    if compute_dev:
        next_dev_version, _ = compute_semver(
            release_version, release='minor', compute_dev=False)
        next_dev_version = '{}dev'.format(next_dev_version)

    return release_version, next_dev_version


def flags_to_release(is_minor=False, is_major=False):
    """Convert flags to release type."""
    if is_minor and is_major:
        raise ValueError("Both `is_minor` and `is_major` are set to 'True'.")

    if is_minor:
        return 'minor'
    if is_major:
        return 'major'
    return 'normal'
