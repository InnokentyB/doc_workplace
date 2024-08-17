import json
from collections import Counter

# Function to process the JSON file and count roles
def count_roles_in_active_positions(json_file_path):
    try:
        # Load JSON data from the file
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        # Navigate to the 'company' -> 'active_positions' section
        active_positions = data.get('company', {}).get('active_positions', [])

        # Extract all the roles from the active positions
        roles = [position.get('role', 'Unknown') for position in active_positions]

        # Count the occurrences of each role
        role_counts = Counter(roles)

        # Print the results
        print("Role Counts in Active Positions:")
        for role, count in role_counts.items():
            print(f"{role}: {count}")

    except FileNotFoundError:
        print(f"Error: The file '{json_file_path}' was not found.")
    except json.JSONDecodeError:
        print("Error: The file is not a valid JSON.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Specify the path to your JSON file
json_file_path = '/content/evo-bank.json'

# Call the function to count roles
count_roles_in_active_positions(json_file_path)
