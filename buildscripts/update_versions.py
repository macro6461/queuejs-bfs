import sys
import json
import re
import subprocess

def get_git_version():
    try:
        result = subprocess.run(['git', 'describe', '--long', '--tags'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        git_output = result.stdout.decode('utf-8').strip()

        match = re.match(r'(\d+\.\d+\.\d+)-(\d+)-g([a-f0-9]+)', git_output)

        if match:
            version = match.group(1)
            commit_count = int(match.group(2))

            version_parts = version.split(".")
            version_parts[2] = str(int(version_parts[2]) + commit_count)
            new_version = ".".join(version_parts)
            
            return new_version
        else:
            print("Error: Could not parse version string from git describe.")
            return None

    except subprocess.CalledProcessError as e:
        print(f"Error running git describe: {e}")
        return None

def update_versions(version=None):
    if not version:
        version = get_git_version()

    if version:
        # Update version in README.md
        with open('README.md', 'r') as file:
            content = file.read()
        content = re.sub(r'v\d+\.\d+\.\d+', 'v'+version, content)
        with open('README.md', 'w') as file:
            file.write(content)

        # Update version in CHANGELOG.md
        with open('CHANGELOG.md', 'r') as file:
            changelog = file.read()
        changelog = re.sub(r'## Version \d+\.\d+\.\d+', f'## Version {version}', changelog, 1)
        with open('CHANGELOG.md', 'w') as file:
            file.write(changelog)

        # Update version in package.json
        with open('package.json', 'r') as file:
            package_data = json.load(file)
        package_data['version'] = version
        with open('package.json', 'w') as file:
            json.dump(package_data, file, indent=4)
        
        print("VERSION: ", version)
        tag_repo(version, "Updated to version " + version + '.')
    else:
        print("No version found, cannot update versions.")

def tag_repo(tag_name, message=None):
    try:
        # Check if the tag already exists
        result = subprocess.run(["git", "tag", "-l", tag_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.stdout.decode("utf-8").strip():
            print(f"Tag {tag_name} already exists, skipping tag creation.")
        else:
            if message:
                subprocess.run(["git", "tag", "-a", tag_name, "-m", message], check=True)
            else:
                subprocess.run(["git", "tag", tag_name], check=True)

        subprocess.run(["git", "push", "origin", tag_name], check=True)
        return tag_name
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while tagging the repository: {e}")

if __name__ == "__main__":
    # Get version from command line argument or run get_git_version if not provided
    version = sys.argv[1] if len(sys.argv) > 1 else None
    update_versions(version)