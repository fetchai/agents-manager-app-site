#!/usr/bin/env python3
import argparse
import json
import re
import sys
import os


PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
VERSIONS_PATH = os.path.join(PROJECT_PATH, 'versions.json')


def _version(text: str) -> str:
    if re.match(r'\d+\.\d+\.\d+', text) is None:
        print(f'Unknown version string: {text}')
        sys.exit(1)
    return text


def parse_commandline() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('next_version', metavar='VERSION', help='The next version to be added to the list')
    return parser.parse_args()


def main():
    args = parse_commandline()

    # read the contents of the versions file
    with open(VERSIONS_PATH, 'r') as versions_file:
        versions = json.load(versions_file)

    # skip the update if the same
    if args.next_version == versions['latest']:
        return

    # sanity checks
    assert args.next_version not in versions['previous']
    assert versions['latest'] not in versions['previous']

    # add the current latest to the previous releases list and add update the latest
    versions['previous'] = [versions['latest']] + versions['previous']
    versions['latest'] = args.next_version

    # write out the file again
    with open(VERSIONS_PATH, 'w') as versions_file:
        json.dump(versions, versions_file)


if __name__ == '__main__':
    main()
