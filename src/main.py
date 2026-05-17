from config_loader import load_system_prompt


# Test loader in config_loader.py
def main() -> None:
  system_prompt = load_system_prompt()

  print("Assignment 2 Part 2 Agent")
  print("System prompt loaded successfully.")
  print()
  print("First 300 characters of system prompt:")
  print(system_prompt[:300])


if __name__ == "__main__":
  main()

