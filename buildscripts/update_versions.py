import json
import re
import subprocess

def get_git_version():
    try:
        # Run 'git describe' and capture the output
        git_output = subprocess.check_output(["git", "describe", "--long"], universal_newlines=True).strip()
        print(f"Git describe output: {git_output}")

        # Split the version into parts (tag-commits-commitHash)
        version_parts = git_output.split('-')

        # If the version has 3 parts (tag-commits-commitHash), extract them
        if len(version_parts) == 3:
            tag = version_parts[0]  # e.g., 1.0.2
            commits = int(version_parts[1])  # e.g., 1
            commit_hash = version_parts[2][1:]  # Remove 'g' prefix, e.g., 4869857

            # Check if there were commits since the last tag
            if commits > 0:
                # Increment the patch version (you can also change minor or major if needed)
                tag_parts = tag.split('.')
                patch_version = int(tag_parts[2]) + 1
                new_tag = f"{tag_parts[0]}.{tag_parts[1]}.{patch_version}"
                print(f"New version (after commits): {new_tag}")
                return new_tag  # Just return the updated version without commits and commit hash

            else:
                # No commits, version stays the same
                print(f"Version stays the same: {tag}")
                return f"{tag}"

        else:
            print("Unexpected git describe output")
            return None

    except subprocess.CalledProcessError as e:
        print(f"Error running git describe: {e}")
        return None

def update_versions():

    version = get_git_version()

    # Example: Update version in README
    with open('README.md', 'r') as file:
        content = file.read()
    
    # Regex or any method to replace version number
    content = re.sub(r'v\d+\.\d+\.\d+', 'v'+version, content)
    
    with open('README.md', 'w') as file:
        file.write(content)
    
    # Example: Update version in changelog
    with open('CHANGELOG.md', 'r') as file:
        changelog = file.read()
    
    changelog = re.sub(r'## Version \d+\.\d+\.\d+', f'## Version {version}', changelog, 1)
    
    with open('CHANGELOG.md', 'w') as file:
        file.write(changelog)
    
    # Example: Update version in package.json
    with open('package.json', 'r') as file:
        package_data = json.load(file)
    
    package_data['version'] = version
    
    with open('package.json', 'w') as file:
        json.dump(package_data, file, indent=4)
    tag_repo(version, "Updated to version " + version + '.')


def tag_repo(tag_name, message=None):
    # Create a new Git tag
    try:
        # Create the tag (you can add a message using '-m' if needed)
        if message:
            subprocess.run(["git", "tag", "-a", tag_name, "-m", message], check=True)
        else:
            subprocess.run(["git", "tag", tag_name], check=True)

        # Push the tag to the remote repository
        subprocess.run(["git", "push", "origin", tag_name], check=True)

        print(f"Successfully tagged the repository with {tag_name}.")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while tagging the repository: {e}")

if __name__ == "__main__":
    update_versions()