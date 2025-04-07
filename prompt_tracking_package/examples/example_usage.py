from prompt_tracking_package.tracker import PromptTracker
import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

tracker = PromptTracker()
user_input = input("Prompt: ")
while user_input != "~~~":
    tracker.track(user_input)
    user_input = input("Prompt: ")
tracker.save_prompt_history()
print("Prompt History Saved")
