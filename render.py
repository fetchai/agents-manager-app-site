#!/usr/bin/env python3
import fnmatch
import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
TEMPLATES_PATH = os.path.join(PROJECT_PATH, "templates")

# The "docs" name of the folder is required by Github Pages
# https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site#choosing-a-publishing-source
PUBLIC_PATH = os.path.join(PROJECT_PATH, "docs")
VERSIONS_PATH = os.path.join(PROJECT_PATH, "versions.json")

BASE_URL = "https://storage.googleapis.com/fetch-ai-aea-manager/releases"
WINDOWS_TEMPLATE = "{base_url}/{version}/AEA Manager Setup {version}.exe"
MACOS_TEMPLATE = "{base_url}/{version}/AEA Manager-{version}.dmg"
RPM_TEMPLATE = "{base_url}/{version}/aea_manager-{version}.x86_64.rpm"
DEB_TEMPLATE = "{base_url}/{version}/aea_manager_{version}_amd64.deb"


def main():
    with open(VERSIONS_PATH, "r") as versions_file:
        versions = json.load(versions_file)

    env = Environment(
        loader=FileSystemLoader(TEMPLATES_PATH),
        autoescape=select_autoescape()
    )

    # build up the render context
    ctx = {
        'versions': versions,
        'urls': {
            'windows': WINDOWS_TEMPLATE.format(base_url=BASE_URL, version=versions['latest']),
            'macos': MACOS_TEMPLATE.format(base_url=BASE_URL, version=versions['latest']),
            'rpm': RPM_TEMPLATE.format(base_url=BASE_URL, version=versions['latest']),
            'deb': DEB_TEMPLATE.format(base_url=BASE_URL, version=versions['latest']),
        }
    }

    for root, _, files in os.walk(TEMPLATES_PATH):
        for file_path in files:
            input_path = os.path.relpath(os.path.join(root, file_path), TEMPLATES_PATH)
            output_path = os.path.join(PUBLIC_PATH, input_path)

            # read and render the template
            template = env.get_template(input_path)
            with open(output_path, "w") as output_file:
                output_file.write(template.render(**ctx))

            print(f"Rendered: {os.path.relpath(output_path, PUBLIC_PATH)}")


if __name__ == "__main__":
    main()
