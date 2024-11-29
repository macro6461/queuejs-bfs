import json
import re
import subprocess

def get_git_version():
    try:
        # Run the `git describe --long` command
        git_output = subprocess.check_output(["git", "describe", "--long"]).decode("utf-8").strip()
        
        # Split the output by "-" and take the first three parts
        version_parts = git_output.split("-")
        
        if len(version_parts) < 4:
            print("Error: Not enough parts in git describe output.")
            return None
        
        # Split the first part (which is the version) by "." and keep the first three parts
        version_numbers = version_parts[0].split(".")
        
        if len(version_numbers) < 3:
            print("Error: Version part format incorrect.")
            return None
        
        # Get the major, minor, patch numbers and the commit count
        version = f"{version_numbers[0]}.{version_numbers[1]}.{int(version_numbers[2]) + int(version_parts[1])}"
        
        return version
    
    except subprocess.CalledProcessError as e:
        print(f"Error running git describe: {e}")
        return None

def update_versions():

    version = get_git_version()

    # Example: Update version in README
    with open('README.md', 'r') as file:
        content = file.read()
    
    # Regex or any method to replace version number
    content = re.sub(r'v\d+\.\d+\.\d+', version, content)
    
    with open('README.md', 'w') as file:
        file.write(content)
    
    # Example: Update version in changelog
    with open('CHANGELOG.md', 'r') as file:
        changelog = file.read()
    
    changelog = re.sub(r'v\d+\.\d+\.\d+', 'v2.0.0', changelog)
    
    with open('CHANGELOG.md', 'w') as file:
        file.write(changelog)
    
    # Example: Update version in package.json
    with open('package.json', 'r') as file:
        package_data = json.load(file)
    
    package_data['version'] = '2.0.0'
    
    with open('package.json', 'w') as file:
        json.dump(package_data, file, indent=4)

if __name__ == "__main__":
    update_versions()