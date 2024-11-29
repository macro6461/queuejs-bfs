import json
import re
import subprocess

def get_git_version():
    # Run the git describe command to get the latest tag and commit count
    try:
        result = subprocess.run(['git', 'describe', '--long', '--tags'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        git_output = result.stdout.decode('utf-8').strip()

        # Parse the version string, commit count, and commit hash from the describe output
        match = re.match(r'(\d+\.\d+\.\d+)-(\d+)-g([a-f0-9]+)', git_output)

        if match:
            version = match.group(1)  # e.g., 1.0.1
            commit_count = int(match.group(2))  # e.g., 11

            # Increment the patch version
            version_parts = version.split(".")
            version_parts[2] = str(int(version_parts[2]) + commit_count)  # Increment patch by commit count
            new_version = ".".join(version_parts)
            
            return new_version
        else:
            print("Error: Could not parse version string from git describe.")
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