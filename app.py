import re
from cs50 import SQL
from flask import Flask, render_template, request, session

# Define a whitelist regular expression that includes Finnish characters and a comma
whitelist_pattern = r'^[a-zA-ZäÄöÖåÅ,]+$'

def valid_input(input_string):
    # Use the whitelist pattern to validate the input
    return re.match(whitelist_pattern, input_string) is not None

# Configure application
app = Flask(__name__)
app.secret_key = '4hH+C4g*7YAv'

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///words.db")

# Run flask web up with methods GET and POST
@app.route("/", methods=["GET", "POST"])
def index():
    part = session.get("part_sp", default=None)
    word_quantity = session.get("word_quantity", default=None)
    ending = session.get("ending", default=None)
    case = session.get("case", default=None)

    if request.method == "POST":
        part = request.form.get("part_sp")
        session["part_sp"] = part

        # Check if part of speech is a string and matches the whitelist pattern
        if not part:
            return render_template("index.html")
        elif not valid_input(part):
            return render_template("error.html")

        word_quantity = request.form.get("word_quantity")
        session["word_quantity"] = word_quantity

        # Check if word_quantity is a valid integer
        try:
            word_quantity = int(word_quantity)
            if word_quantity < 1 or word_quantity > 500:
                return render_template("error.html")
        except ValueError:
            return render_template("error.html")

        # Check user's endings
        ending = request.form.get("ending")
        session["ending"] = ending
        if ending:
            if not valid_input(ending):
                return render_template("error.html")

        case = request.form.get("case")
        session["case"] = case

        # Check user's case
        if not case:
            return render_template("index.html")
        elif not valid_input(case):
            return render_template("error.html")

        elif case == 'all':
            # Define the first query template without LIMIT
            count_query = """
            WITH CTE AS (
            SELECT nav.word, nav.type, tfe.translation,
                    ROW_NUMBER() OVER (PARTITION BY nav.word) AS row_num
            FROM noun_adj_verb AS nav
            JOIN frek AS f ON nav.word = f.word
            JOIN translation_fi_en AS tfe ON nav.word = tfe.word
            WHERE (? = 'all' OR nav.type = ?) AND ({ending_condition})
            )
            SELECT COUNT(*) AS total_count
            FROM CTE
            WHERE row_num = 1;
            """

            # Define the base query template with placeholders for part=all and case=all and word_quantity, remove duplicates
            base_query = """
            WITH CTE AS (
            SELECT nav.word, nav.type, tfe.translation, f.number,
                    ROW_NUMBER() OVER (PARTITION BY nav.word) AS row_num
            FROM noun_adj_verb AS nav
            JOIN frek AS f ON nav.word = f.word
            JOIN translation_fi_en AS tfe ON nav.word = tfe.word
            WHERE (? = 'all' OR nav.type = ?) AND ({ending_condition})
            )
            SELECT word, type, translation, number
            FROM CTE
            WHERE row_num = 1
            ORDER BY (
            SELECT f.number
            FROM frek AS f
            WHERE f.word = CTE.word
            )
            LIMIT ?;
            """

        elif case == 'short':
            # Define the base query template with placeholders for part, word_quantity, short case
            count_query = """
            WITH CTE AS (
            SELECT nav.word, nav.type, tfe.translation, ots.word,
                    ROW_NUMBER() OVER (PARTITION BY nav.word) AS row_num
            FROM noun_adj_verb AS nav
            JOIN frek AS f ON nav.word = f.word
            JOIN translation_fi_en AS tfe ON nav.word = tfe.word
            JOIN one_two_syl AS ots ON nav.word = ots.word
            WHERE (? = 'all' OR nav.type = ?) AND ({ending_condition})
            )
            SELECT COUNT(*) AS total_count
            FROM CTE
            WHERE row_num = 1;
            """

            # Define the base query template with placeholders for part=all and case=all and word_quantity, remove duplicates
            base_query = """
            WITH CTE AS (
            SELECT nav.word, nav.type, tfe.translation, f.number,
                    ROW_NUMBER() OVER (PARTITION BY nav.word) AS row_num
            FROM noun_adj_verb AS nav
            JOIN frek AS f ON nav.word = f.word
            JOIN translation_fi_en AS tfe ON nav.word = tfe.word
            JOIN one_two_syl AS ots ON nav.word = ots.word
            WHERE (? = 'all' OR nav.type = ?) AND ({ending_condition})
            )
            SELECT word, type, translation, number
            FROM CTE
            WHERE row_num = 1
            ORDER BY (
            SELECT f.number
            FROM frek AS f
            WHERE f.word = CTE.word
            )
            LIMIT ?;
            """

        elif case == 'long':
            # Define the first query template without LIMIT
            count_query = """
            WITH CTE AS (
            SELECT nav.word, nav.type, tfe.translation,
                    ROW_NUMBER() OVER (PARTITION BY nav.word) AS row_num
            FROM noun_adj_verb AS nav
            LEFT JOIN frek AS f ON nav.word = f.word
            LEFT JOIN translation_fi_en AS tfe ON nav.word = tfe.word
            LEFT JOIN one_two_syl AS ots ON nav.word = ots.word
            WHERE (? = 'all' OR nav.type = ?) AND ({ending_condition}) AND ots.word IS NULL AND f.number IS NOT NULL AND tfe.translation IS NOT NULL
            )
            SELECT COUNT(*) AS total_count
            FROM CTE
            WHERE row_num = 1;
            """

            # Define the base query template with placeholders for part=all and case=long and word_quantity, remove duplicates
            base_query = """
            WITH CTE AS (
            SELECT nav.word, nav.type, tfe.translation, f.number,
                    ROW_NUMBER() OVER (PARTITION BY nav.word) AS row_num
            FROM noun_adj_verb AS nav
            LEFT JOIN frek AS f ON nav.word = f.word
            LEFT JOIN translation_fi_en AS tfe ON nav.word = tfe.word
            LEFT JOIN one_two_syl AS ots ON nav.word = ots.word
            WHERE (? = 'all' OR nav.type = ?) AND ({ending_condition}) AND ots.word IS NULL AND f.number IS NOT NULL AND tfe.translation IS NOT NULL
            )
            SELECT word, type, translation, number
            FROM CTE
            WHERE row_num = 1
            ORDER BY (
            SELECT f.number
            FROM frek AS f
            WHERE f.word = CTE.word
            )
            LIMIT ?;
            """

        elif case == 'old':
            # Define the first query template without LIMIT
            count_query = """
            WITH CTE AS (
            SELECT nav.word, nav.type, tfe.translation,
                    ROW_NUMBER() OVER (PARTITION BY nav.word) AS row_num
            FROM noun_adj_verb AS nav
            JOIN frek AS f ON nav.word = f.word
            JOIN translation_fi_en AS tfe ON nav.word = tfe.word
            JOIN i_noun_adj_old_new AS inaon ON nav.word = inaon.word
            WHERE (? = 'all' OR nav.type = ?) AND ({ending_condition}) AND inaon.age = 'old'
            )
            SELECT COUNT(*) AS total_count
            FROM CTE
            WHERE row_num = 1;
            """

            # Define the base query template with placeholders for part=all and case=old and word_quantity, remove duplicates
            base_query = """
            WITH CTE AS (
            SELECT nav.word, nav.type, tfe.translation, f.number,
                    ROW_NUMBER() OVER (PARTITION BY nav.word) AS row_num
            FROM noun_adj_verb AS nav
            JOIN frek AS f ON nav.word = f.word
            JOIN translation_fi_en AS tfe ON nav.word = tfe.word
            JOIN i_noun_adj_old_new AS inaon ON nav.word = inaon.word
            WHERE (? = 'all' OR nav.type = ?) AND ({ending_condition}) AND inaon.age = 'old'
            )
            SELECT word, type, translation, number
            FROM CTE
            WHERE row_num = 1
            ORDER BY (
            SELECT f.number
            FROM frek AS f
            WHERE f.word = CTE.word
            )
            LIMIT ?;
            """

        elif case == 'new':
            # Define the first query template without LIMIT
            count_query = """
            WITH CTE AS (
            SELECT nav.word, nav.type, tfe.translation,
                    ROW_NUMBER() OVER (PARTITION BY nav.word) AS row_num
            FROM noun_adj_verb AS nav
            JOIN frek AS f ON nav.word = f.word
            JOIN translation_fi_en AS tfe ON nav.word = tfe.word
            JOIN i_noun_adj_old_new AS inaon ON nav.word = inaon.word
            WHERE (? = 'all' OR nav.type = ?) AND ({ending_condition}) AND inaon.age = 'new'
            )
            SELECT COUNT(*) AS total_count
            FROM CTE
            WHERE row_num = 1;
            """

            # Define the base query template with placeholders for part=all and case=all and word_quantity, remove duplicates
            base_query = """
            WITH CTE AS (
            SELECT nav.word, nav.type, tfe.translation, f.number,
                    ROW_NUMBER() OVER (PARTITION BY nav.word) AS row_num
            FROM noun_adj_verb AS nav
            JOIN frek AS f ON nav.word = f.word
            JOIN translation_fi_en AS tfe ON nav.word = tfe.word
            JOIN i_noun_adj_old_new AS inaon ON nav.word = inaon.word
            WHERE (? = 'all' OR nav.type = ?) AND ({ending_condition}) AND inaon.age = 'new'
            )
            SELECT word, type, translation, number
            FROM CTE
            WHERE row_num = 1
            ORDER BY (
            SELECT f.number
            FROM frek AS f
            WHERE f.word = CTE.word
            )
            LIMIT ?;
            """

        elif case == 'hauska':
            # Define the first query template without LIMIT
            count_query = """
            WITH CTE AS (
            SELECT nav.word, nav.type, tfe.translation,
                    ROW_NUMBER() OVER (PARTITION BY nav.word) AS row_num
            FROM noun_adj_verb AS nav
            JOIN frek AS f ON nav.word = f.word
            JOIN translation_fi_en AS tfe ON nav.word = tfe.word
            JOIN two_syl_hauska AS tsh ON nav.word = tsh.word
            WHERE (? = 'all' OR nav.type = ?) AND ({ending_condition}) AND tsh.type_2 = 'hauska'
            )
            SELECT COUNT(*) AS total_count
            FROM CTE
            WHERE row_num = 1;
            """

            # Define the base query template with placeholders for part=all and case=hauska and word_quantity, remove duplicates
            base_query = """
            WITH CTE AS (
            SELECT nav.word, nav.type, tfe.translation, f.number,
                    ROW_NUMBER() OVER (PARTITION BY nav.word) AS row_num
            FROM noun_adj_verb AS nav
            JOIN frek AS f ON nav.word = f.word
            JOIN translation_fi_en AS tfe ON nav.word = tfe.word
            JOIN two_syl_hauska AS tsh ON nav.word = tsh.word
            WHERE (? = 'all' OR nav.type = ?) AND ({ending_condition}) AND tsh.type_2 = 'hauska'
            )
            SELECT word, type, translation, number
            FROM CTE
            WHERE row_num = 1
            ORDER BY (
            SELECT f.number
            FROM frek AS f
            WHERE f.word = CTE.word
            )
            LIMIT ?;
            """

        elif case == 'koira':
             # Define the first query template without LIMIT
            count_query = """
            WITH CTE AS (
            SELECT nav.word, nav.type, tfe.translation,
                    ROW_NUMBER() OVER (PARTITION BY nav.word) AS row_num
            FROM noun_adj_verb AS nav
            JOIN frek AS f ON nav.word = f.word
            JOIN translation_fi_en AS tfe ON nav.word = tfe.word
            JOIN two_syl_hauska AS tsh ON nav.word = tsh.word
            WHERE (? = 'all' OR nav.type = ?) AND ({ending_condition}) AND tsh.type_2 = 'koira'
            )
            SELECT COUNT(*) AS total_count
            FROM CTE
            WHERE row_num = 1;
            """

            # Define the base query template with placeholders for part=all and case=koira and word_quantity, remove duplicates
            base_query = """
            WITH CTE AS (
            SELECT nav.word, nav.type, tfe.translation, f.number,
                    ROW_NUMBER() OVER (PARTITION BY nav.word) AS row_num
            FROM noun_adj_verb AS nav
            JOIN frek AS f ON nav.word = f.word
            JOIN translation_fi_en AS tfe ON nav.word = tfe.word
            JOIN two_syl_hauska AS tsh ON nav.word = tsh.word
            WHERE (? = 'all' OR nav.type = ?) AND ({ending_condition}) AND tsh.type_2 = 'koira'
            )
            SELECT word, type, translation, number
            FROM CTE
            WHERE row_num = 1
            ORDER BY (
            SELECT f.number
            FROM frek AS f
            WHERE f.word = CTE.word
            )
            LIMIT ?;
            """

        # Split the input endings by commas and add them to the query
        endings = [e.strip() for e in ending.split(',')]

        # Create a list to hold the conditions for each ending
        ending_conditions = []
        for end in endings:
            # Append a condition for each ending
            ending_conditions.append("(nav.word LIKE ?)")

        # Combine the ending conditions using "OR"
        ending_condition = " OR ".join(ending_conditions)

        # Replace placeholders and execute the query
        count_parameters = [part, part] + [f'%{end}' for end in endings]

        # Replace placeholders and execute the query
        query_parameters = [part, part] + [f'%{end}' for end in endings] + [word_quantity]

        # Manually replace the placeholder in the SQL query
        count_query = count_query.replace('{ending_condition}', ending_condition)

        # Manually replace the placeholder in the SQL query
        base_query = base_query.replace('{ending_condition}', ending_condition)

        # Execute the querys with placeholders
        total_count = db.execute(count_query, *count_parameters)[0]['total_count']
        words = db.execute(base_query, *query_parameters)

        # Assuming 'words' is a list of dictionaries containing word information
        for i, word in enumerate(words, start=1):
            word['row_number'] = i

        return render_template("index.html", words=words, total_count=total_count, part=part, case=case, ending=ending, word_quantity=word_quantity)
    else:
        return render_template("index.html")

@app.route("/about")
def about():
    """About page"""
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
