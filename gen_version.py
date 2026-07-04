import os
from lib.utils.version import CAVersion

version = CAVersion.get_latest_release_version()

os.makedirs('lib', exist_ok=True)

output_path = 'lib/version.py'
print(f"Writing version to: {os.path.abspath(output_path)}")

with open(output_path, 'w') as f:
    f.write(f'__version__ = "{version}"\n')

print("Done!")
