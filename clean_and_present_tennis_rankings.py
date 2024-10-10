
#Not part of actual codebase.
import json

def load_rankings():
    # Load the saved rankings data
    with open("rankings.json", "r") as file:
        rankings_data = json.load(file)
    return rankings_data

# Use the loaded rankings data
rankings = load_rankings()
pretty_json = json.dumps(rankings, indent=4)
print(pretty_json)
