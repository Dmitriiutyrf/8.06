import subprocess
import os
import sys

class Scanner:
    def __init__(self, engine_root=None):
        if engine_root is None:
            # Default to the 'engine' folder in the same directory as bridge.py
            self.engine_root = os.path.join(os.path.dirname(__file__), "engine")
        else:
            self.engine_root = engine_root

        self.script_path = os.path.join(
            self.engine_root, "skills", "last30days", "scripts", "last30days.py"
        )
        self.python_exe = sys.executable

    def scan(self, topic):
        """Runs the OSINT scan and returns the result."""
        if not os.path.exists(self.script_path):
            return f"Error: Engine script not found at {self.script_path}"

        cmd = [
            self.python_exe,
            self.script_path,
            topic,
            "--emit=compact"
        ]

        # Ensure the environment has the necessary context
        env = os.environ.copy()

        # Add the scripts/lib folder to PYTHONPATH so engine can find its modules
        lib_path = os.path.join(self.engine_root, "skills", "last30days", "scripts")
        if "PYTHONPATH" in env:
            env["PYTHONPATH"] = f"{lib_path}{os.pathsep}{env['PYTHONPATH']}"
        else:
            env["PYTHONPATH"] = lib_path

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                env=env,
                cwd=lib_path,
                check=False
            )

            if result.returncode != 0:
                return f"Error running scan:\n{result.stderr}"

            return result.stdout
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        scanner = Scanner()
        print(scanner.scan(sys.argv[1]))
    else:
        print("Usage: python bridge.py <topic>")
