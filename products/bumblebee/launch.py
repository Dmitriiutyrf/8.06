import subprocess
import sys
import shutil

def check_bumblebee():
    if shutil.which("bumblebee"):
        return True
    return False

def run_scan():
    print("--- Bumblebee AI Security Scanner ---")
    if not check_bumblebee():
        print("Error: 'bumblebee' binary not found.")
        print("Please install it first: go install github.com/perplexityai/bumblebee/cmd/bumblebee@latest")
        sys.exit(1)

    print("Running baseline security scan...")
    try:
        # Run baseline scan and output to stdout
        subprocess.run(["bumblebee", "scan", "--profile", "baseline"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Scan failed with error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_scan()
