import re
import os


class CAVersion:

    @staticmethod
    def get_latest_release_version(changelog_path='CHANGELOG.md', verbose=False):
        print(f"Reading changelog from: {os.path.abspath(changelog_path)}") if verbose else None
        with open(changelog_path, 'r') as file:
            content = file.read()
        versions = re.findall(r'\[\d+\.\d+\.\d+\]', content)
        if not versions:
            return "0.0.0"
        return versions[0].strip('[]')