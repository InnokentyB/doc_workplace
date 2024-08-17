mport csv
import requests
import random
import string

# File paths
input_file_path = '/content/for API.csv'
output_file_path = '/content/output_file.csv'

# Define the base URL for the REST API
base_url = "https://aiws.infocamere.it/aiws/rest/registroimprese/output/impresa/blocchi/nrea/xml"

# Function to generate random string for username and password
def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Function to make the API request
def get_api_response(province, nreanum):
    # Replace placeholders with actual values
    url = f"{base_url}?cciaa={province}&nRea={nreanum}&blocco=SOC"

    # Generate random username and password
    username = ''
    password = '!'

    # Define the headers
    headers = {
        'username': username,
        'password': password
    }

    try:
        # Make the GET request with headers
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {province} and {nreanum}: {e}")
        return None

# Read the input CSV, process it, and save the results to the output CSV
with open(input_file_path, 'r') as infile, open(output_file_path, 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Write the header
    header = next(reader)
    new_header = header + ['API Response']
    writer.writerow(new_header)

    # Process each row
    for row in reader:
        province = row[1]
        nreanum = row[2]

        # Get the API response
        api_response = get_api_response(province, nreanum)

        # Append the response to the row and write to the output file
        new_row = row + [api_response]
        writer.writerow(new_row)

print(f"Processed file saved as {output_file_path}")
