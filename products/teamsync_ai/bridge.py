import os
import shutil
from datetime import datetime

class GNAPProtocol:
    def __init__(self, board_root=None):
        self.board_root = board_root or os.path.join(os.path.dirname(__file__), "board")
        self.todo_dir = os.path.join(self.board_root, "todo")
        self.doing_dir = os.path.join(self.board_root, "doing")
        self.done_dir = os.path.join(self.board_root, "done")

        # Ensure directories exist
        for d in [self.todo_dir, self.doing_dir, self.done_dir]:
            os.makedirs(d, exist_ok=True)

    def create_task(self, title, description, agent="coordinator"):
        """Creates a new task in the todo folder."""
        filename = f"{title.lower().replace(' ', '-')}.md"
        filepath = os.path.join(self.todo_dir, filename)
        content = f"# Task: {title}\n\n**Created:** {datetime.now()}\n**Creator:** {agent}\n\n## Description\n{description}\n"
        with open(filepath, "w") as f:
            f.write(content)
        return filename

    def claim_task(self, filename, agent):
        """Moves a task from todo to doing."""
        src = os.path.join(self.todo_dir, filename)
        dst = os.path.join(self.doing_dir, filename)
        if os.path.exists(src):
            with open(src, "a") as f:
                f.write(f"\n**Claimed by:** {agent}\n**Started:** {datetime.now()}\n")
            shutil.move(src, dst)
            return True
        return False

    def complete_task(self, filename, result):
        """Moves a task from doing to done with result."""
        src = os.path.join(self.doing_dir, filename)
        dst = os.path.join(self.done_dir, filename)
        if os.path.exists(src):
            with open(src, "a") as f:
                f.write(f"\n## Result\n{result}\n**Completed:** {datetime.now()}\n")
            shutil.move(src, dst)
            return True
        return False

    def get_status(self):
        """Returns the current board status."""
        return {
            "todo": os.listdir(self.todo_dir),
            "doing": os.listdir(self.doing_dir),
            "done": os.listdir(self.done_dir)
        }

if __name__ == "__main__":
    gnap = GNAPProtocol()
    task = gnap.create_task("Analyze Market", "Use ShadowPulse to analyze AI video market.")
    print(f"Created task: {task}")
    print(f"Status: {gnap.get_status()}")
