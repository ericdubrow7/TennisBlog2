import json

def add_post_to_json(file_path, new_post):
    try:
        # Load existing data from the JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Add the new post to the list
        data.insert(0, new_post)

        # Write the updated data back to the JSON file
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

        print("Post added successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")