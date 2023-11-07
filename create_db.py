import sqlite3

# Define the schema
schema = {
    "translation_fi_en": [
        ("word", "TEXT UNIQUE"),
        ("type", "TEXT"),
        ("translation", "TEXT")
    ],
    "frek": [
        ("word", "TEXT UNIQUE"),
        ("number", "INTEGER"),
        ("abs", "INTEGER"),
    ],
    "noun_adj_verb": [
        ("word", "TEXT"),
        ("type", "TEXT"),
    ],
    "i_noun_adj_old_new": [
        ("word", "TEXT UNIQUE"),
        ("type", "TEXT"),
        ("age", "TEXT"),
    ],
    "one_two_syl": [
        ("word", "TEXT UNIQUE"),
        ("type", "TEXT"),
    ],
    "two_syl_hauska": [
        ("word", "TEXT UNIQUE"),
        ("type", "TEXT"),
        ("type_2", "TEXT"),
    ],
}

# Connect to the database (it will be created if it doesn't exist)
conn = sqlite3.connect('words.db')
cursor = conn.cursor()

# Create tables based on the schema
for table_name, columns in schema.items():
    create_table_sql = f"CREATE TABLE {table_name} ({', '.join([f'{col} {type}' for col, type in columns])})"
    cursor.execute(create_table_sql)

    # Add an index to the 'word' column for each table
    cursor.execute(f"CREATE INDEX idx_{table_name}_word ON {table_name} (word)")

# Commit the changes and close the connection
conn.commit()
conn.close()
