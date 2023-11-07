import sqlite3
import csv

# Define a dictionary with table names and their corresponding CSV file paths
table_files = {
    "translation_fi_en": "/workspaces/121390506/final/source/01_translation_fi_en.csv",
    "frek": "/workspaces/121390506/final/source/02_parole_frek_3_filtered2.csv",
    "noun_adj_verb": "/workspaces/121390506/final/source/03_noun_adj_verb.csv",
    "i_noun_adj_old_new": "/workspaces/121390506/final/source/04_i_noun_adj_old_new.csv",
    "one_two_syl": "/workspaces/121390506/final/source/05_one_two_syl.csv",
    "two_syl_hauska": "/workspaces/121390506/final/source/06_finnish_two-syllable_a_words_part_hauska_koira.csv",
}

# Connect to your SQLite database
conn = sqlite3.connect('words.db')
cursor = conn.cursor()

# Iterate through the dictionary and fill the tables
for table, file_path in table_files.items():
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)  # Read the header row

        # Filter the columns based on your schema
        filtered_rows = []
        for row in csv_reader:
            # Ensure only the expected columns are included
            filtered_row = row[:len(header)]
            filtered_rows.append(filtered_row)

        # Create an INSERT query based on the table's columns
        insert_query = f"INSERT INTO {table} VALUES ({', '.join(['?'] * len(header))})"

        for row in filtered_rows:
            cursor.execute(insert_query, row)

# Commit the changes and close the connection
conn.commit()
conn.close()
