import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

EXCLUDE = {'__pycache__', 'scripts', 'integrations', 'examples', 'strategy'}

def launch():
    print("--- Agency Agents Launcher ---")
    print("Available categories:")
    categories = sorted([d for d in os.listdir(BASE_DIR)
                         if os.path.isdir(os.path.join(BASE_DIR, d))
                         and not d.startswith('.')
                         and d not in EXCLUDE])
    for i, cat in enumerate(categories):
        print(f"{i+1}. {cat}")

    print("\nSelect a category to see agents or read GUIDE.md for instructions.")

if __name__ == "__main__":
    launch()
