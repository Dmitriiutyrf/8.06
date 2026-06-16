import os

def launch():
    print("--- Agency Agents Launcher ---")
    print("Available categories:")
    categories = [d for d in os.listdir('.') if os.path.isdir(d) and not d.startswith('.')]
    for i, cat in enumerate(categories):
        print(f"{i+1}. {cat}")

    print("\nSelect a category to see agents or read GUIDE.md for instructions.")

if __name__ == "__main__":
    launch()
