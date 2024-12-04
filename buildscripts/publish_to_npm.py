import os
import subprocess
import shutil


def publish_to_npm():
    print("CHECKING NPM TOKEN!!")
    npm_token = os.getenv("NPM_TOKEN")
    if not npm_token:
        print("NPM_TOKEN is not set. Exiting...")
        exit(-1)
    print(f"NPM_TOKEN: {npm_token}")

    print("Publishing to NPM...")

    # Check if NVM is installed
    nvm_path = os.path.expanduser("~/.nvm/nvm.sh")
    if not os.path.exists(nvm_path):
        print("This build requires NVM to be installed.")
        exit(-1)

    # Install NVM
    print("Installing NVM...")
    os.environ["NVM_DIR"] = os.path.expanduser("~/.nvm")
    subprocess.run(["bash", "-c", f"source {nvm_path} && nvm install"], check=True)

    # Check if yarn.lock exists, create if not
    if not os.path.exists("yarn.lock"):
        print("yarn.lock not found, creating an empty yarn.lock file...")
        with open("yarn.lock", "w") as lockfile:
            lockfile.write("")
    
        subprocess.run(["yarn", "add", "--dev", "@react-native-community/bob"], check=True)
    else:
        print("'bob' is already installed, proceeding to publish.")

    # Run npm publish --dry-run to check for any issues
    print("Performing npm publish dry-run...")
    dry_run_result = subprocess.run(["npm", "publish", "--dry-run"], check=False)
    if dry_run_result.returncode == 0:
        print("Dry-run successful, proceeding to actual publish.")
        publish_result = subprocess.run(["npm", "publish"], check=False)
        if publish_result.returncode == 0:
            print("NPM PUBLISH SUCCEEDED!")
        else:
            print("NPM PUBLISH FAILED!")
            exit(-1)
    else:
        print("Dry-run failed. Please fix the issues before attempting to publish.")
        exit(-1)

    # After publishing, clean up
    print("Initializing cleanup...")
    clean_up()


def clean_up():
    capture_dir = "buildscripts/react-native-capture"
    try:
        os.chdir("..")
        if os.path.exists(capture_dir):
            print(f"Removing {capture_dir}...")
            # Add write permissions to all files and directories before removing
            for root, dirs, files in os.walk(capture_dir):
                for d in dirs:
                    os.chmod(os.path.join(root, d), 0o777)
                for f in files:
                    os.chmod(os.path.join(root, f), 0o777)
            shutil.rmtree(capture_dir)
            print(f"Successfully removed {capture_dir}")
        else:
            print(f"{capture_dir} does not exist. Skipping cleanup.")
    except Exception as e:
        print(f"An error occurred during cleanup: {e}")
        exit(-1)
    finally:
        print("Cleanup is finished.")


if __name__ == "__main__":
    publish_to_npm()