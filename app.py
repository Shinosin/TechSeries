from flask import Flask, jsonify, render_template, request, redirect, url_for
import game
import sqlite3

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/login')
# def login():
#     return


@app.route('/start_pygame')
def start_pygame():
    game.main()
    return render_template('end.html')


# The below section are for pages and function related to foodItem
# reference: https://www.youtube.com/watch?v=m9hUC-WRclU
# For pages
@app.route('/insertFoodItemForm')
def insert_food_item_form():
    return render_template('insertFoodItemForm.html')


@app.route('/result')
def displayResults():
    return render_template('result.html')

# Route to add a new record (INSERT) food item data to the database


@app.route("/insertFoodItem", methods=['POST', 'GET'])
def insertFoodItem():
    msg = ""  # Initialize msg to avoid reference before assignment

    # Data will be available from POST submitted by the form
    if request.method == 'POST':
        try:
            # Get the food item name and expiry date from the form
            foodItemName = request.form['foodItemName']
            expiryDate = request.form['expiryDate']

            # Connect to SQLite3 database and execute the INSERT
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO foodItem (foodItemName, expiryDate) VALUES (?, ?)", (foodItemName, expiryDate))

                con.commit()
                msg = "Record successfully added to database"
        except:
            con.rollback()
            msg = "Error in the INSERT"
        finally:
            con.close()
            # Send the transaction message to result.html
            # After processing POST request, return response
        return redirect("/displayFoodItemList")
        # return render_template('result.html', msg=msg)

    # Render the form if the request method is GET
    return render_template('insertFoodItem.html')


# Route to SELECT all data from the database and display in a table
@app.route('/displayFoodItemList')
def getAllFoodItems():
    # Connect to the SQLite3 datatabase and
    # SELECT rowid and all Rows from the students table.
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute(
        "SELECT id, foodItemName, expiryDate FROM foodItem ORDER BY expiryDate ASC")

    rows = cur.fetchall()
    con.close()
    # Send the results of the SELECT to the list.html page
    return render_template("result.html", rows=rows)


# Route that will SELECT a specific row in the database then load an Edit form
@app.route("/editForm", methods=['POST'])
def editForm():
    if request.method == 'POST':
        try:
            # Use the hidden input value of id from the form to get the rowid
            rowid = request.form['id']

            # Connect to the database and SELECT a specific row by rowid
            with sqlite3.connect('database.db') as con:
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                cur.execute(
                    "SELECT id, foodItemName, expiryDate FROM foodItem WHERE id=?", (rowid,))

                row = cur.fetchone()
                if row:
                    return render_template('insertFoodItemForm.html', is_update=True, foodItemName=row['foodItemName'], expiryDate=row['expiryDate'], id=row['id'])
                else:
                    return "Record not found", 404
        except Exception as e:
            return f"An error occurred: {str(e)}"


# Route used to execute the UPDATE statement on a specific record in the database
@app.route("/editFoodItem", methods=['POST', 'GET'])
def editFoodItem():
    con = None  # Initialize con to None
    if request.method == 'POST':
        try:
            # Use the hidden input value of id from the form to get the rowid
            rowid = request.form['rowid']
            foodItemName = request.form['foodItemName']
            expiryDate = request.form['expiryDate']

            # Connect to the database and update the specific record
            con = sqlite3.connect('database.db')
            cur = con.cursor()
            cur.execute("UPDATE foodItem SET foodItemName=?, expiryDate=? WHERE id=?",
                        (foodItemName, expiryDate, rowid))

            con.commit()
            msg = "Record successfully edited in the database"
        except Exception as e:
            if con:
                con.rollback()
            msg = f"Error in the Edit: {str(e)}"
        finally:
            if con:
                con.close()
            return redirect("/displayFoodItemList")
            # # Send the transaction message to result.html
            # return render_template('result.html', msg=msg)


# Route used to DELETE a specific record in the database
@app.route("/deleteFoodItem", methods=['POST', 'GET'])
def delete():
    if request.method == 'POST':
        try:
            # Use the hidden input value of id from the form to get the rowid
            rowid = request.form['id']
            # Connect to the database and DELETE a specific record based on rowid
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("DELETE FROM foodItem WHERE rowid="+rowid)

                con.commit()
                msg = "Record successfully deleted from the database"
        except:
            con.rollback()
            msg = "Error in the DELETE"

        finally:
            con.close()
            # Send the transaction message to result.html
            return redirect("/displayFoodItemList")


# The below section are for pages and function related to user
# @app.route('/', methods=['GET'])
# def home():
#     return redirect(url_for('show_register_form'))


@app.route('/register', methods=['GET'])
def show_register_form():
    return render_template('register.html')


@app.route('/api/register', methods=['POST'])
def register():
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    if password != confirm_password:
        return render_template('register.html', error="Passwords do not match")

    con = sqlite3.connect('database.db')
    cur = con.cursor()

    try:
        # Check if the email already exists
        cur.execute("SELECT * FROM user WHERE email = ?", (email,))
        existing_user = cur.fetchone()

        if existing_user:
            return render_template('register.html', error="Email already exists")

        # Insert the new user into the database
        cur.execute(
            "INSERT INTO user (email, password) VALUES (?, ?)", (email, password))
        con.commit()
    except Exception as e:
        con.rollback()
        return render_template('register.html', error=f"An error occurred: {str(e)}")
    finally:
        con.close()

    print(f"Registered user: {email}, Password: {password}")
    return render_template('register_success.html', email=email)


@app.route('/login', methods=['GET'])
def login_form():
    return render_template('login.html')


@app.route('/api/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return render_template('login.html', error="Email and password are required")

    con = sqlite3.connect('database.db')
    # This ensures that rows can be accessed like dictionaries
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    try:
        # Retrieve the user's password from the database using the email
        cur.execute("SELECT password FROM user WHERE email = ?", (email,))
        stored_password_row = cur.fetchone()

        if stored_password_row and stored_password_row['password'] == password:
            return render_template('welcome.html', email=email)
        else:
            return render_template('login.html', error="Invalid email or password")

    except Exception as e:
        return f"An error occurred: {str(e)}", 500

    finally:
        con.close()


# The below section are for pages and function related to food donation
# For pages
@app.route('/submitDonation')
def submitDonatioForm():
    # Connect to the SQLite3 database and SELECT the necessary data
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute(
        "SELECT id, foodItemName, expiryDate FROM foodItem ORDER BY expiryDate ASC")

    rows = cur.fetchall()
    con.close()
    # Send the results of the SELECT to the submitDonation.html page
    return render_template("submit.html", rows=rows)


# # Route to add a new record (INSERT) food item data to the database
# @app.route("/insertFoodItem", methods=['POST', 'GET'])
# def insertFoodItem():
#     msg = ""  # Initialize msg to avoid reference before assignment

#     # Data will be available from POST submitted by the form
#     if request.method == 'POST':
#         try:
#             # Get the food item name and expiry date from the form
#             foodItemName = request.form['foodItemName']
#             expiryDate = request.form['expiryDate']

#             # Connect to SQLite3 database and execute the INSERT
#             with sqlite3.connect('database.db') as con:
#                 cur = con.cursor()
#                 cur.execute("INSERT INTO foodItem (foodItemName, expiryDate) VALUES (?, ?)", (foodItemName, expiryDate))

#                 con.commit()
#                 msg = "Record successfully added to database"
#         except:
#             con.rollback()
#             msg = "Error in the INSERT"
#         finally:
#             con.close()
#             # Send the transaction message to result.html
#             # After processing POST request, return response
#         return redirect("/displayFoodItemList")
#         # return render_template('result.html', msg=msg)

#     # Render the form if the request method is GET
#     return render_template('insertFoodItem.html')

@app.route('/donationSuccess')
def submitSuccess():
    return render_template('success.html')


@app.route('/donationCriteria')
def donationCriteria():
    return render_template('criteria.html')


if __name__ == "__main__":
    app.run()
