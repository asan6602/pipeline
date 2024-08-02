import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# List of URLs to scrape
urls = [
    "https://www.baseball-reference.com/teams/NYM/bat.shtml",
    "https://www.baseball-reference.com/teams/NYM/pitch.shtml"  # Replace with your second URL
]

# List of CSV filenames
csv_filenames = [
    'team_nym_batting_stats.csv',
    'team_nym_pitching_stats.csv'  # Ensure this matches the order of URLs
]

# Corresponding HTML element IDs and table IDs
element_ids = [
    {'div_id': 'div_batting_register', 'table_id': 'batting_register'},
    {'div_id': 'div_pitching_register', 'table_id': 'pitching_register'}
]

for url, filename, ids in zip(urls, csv_filenames, element_ids):
    # Send a GET request to the webpage
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the div with the specified id
        table_container = soup.find('div', {'id': ids['div_id']})

        # Find the table with the specified id within the div
        table = table_container.find('table', {'id': ids['table_id']})

        # Extract the headers
        headers = [th.get('data-stat') for th in table.find('thead').find_all('th')]

        # Extract the rows
        rows = table.find('tbody').find_all('tr')

        # Extract data from each row
        data = []
        for row in rows:
            cols = row.find_all('td')
            if cols:  # Skip empty rows
                row_data = [col.text.strip() for col in cols]
                data.append(row_data)

        # Create a DataFrame
        df = pd.DataFrame(data, columns=headers[1:])

        # Define the filename
        filename = os.path.join('csv', filename)

        # Save the DataFrame to a CSV file
        df.to_csv(filename, index=False)
    else:
        print(f"Failed to retrieve the web page from {url}. Status code: {response.status_code}")
