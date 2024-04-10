import os
import re
import sqlite3

from flask import Flask, abort, render_template, url_for, request, flash, redirect, session, jsonify
from cs50 import SQL
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_wtf import FlaskForm
from flask_login import LoginManager, login_user, login_required, UserMixin
from flask_wtf.csrf import CSRFProtect, generate_csrf
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename



app = Flask(__name__)
app.config['SECRET_KEY'] = 'b678#-$fjkLV'

csrf = CSRFProtect(app)
db = SQL("sqlite:///hungrystudentss.db")


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['UPLOAD_FOLDER'] = 'static/img_uploads'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


Session(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, id):
        self.id = id


@login_manager.user_loader
def load_user(user_id):
    user_row = db.execute("SELECT * FROM students WHERE id = ?", user_id)
    if user_row:
        return User(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


@app.route("/login", methods=['POST', 'GET'])
def login():
    session.clear()

    form = LoginForm()
    csrf_token = generate_csrf()
    if form.validate_on_submit():
        password = form.password.data
        email = form.email.data.lower()
        user = db.execute(
            'SELECT * FROM students WHERE email = ?', (email,))[0]
        print("User:", user)

        password_hash = user["password"]
        entered_password = password
        if check_password_hash(password_hash, entered_password):
            # Create a User object based on your User model
            user_obj = User(user["id"])
            # Log in the user
            login_user(user_obj)
            session['student_id'] = user["id"]
            return render_template('index.html')
        else:
            flash('Invalid email or password', 'error')
            print("Password Hash:", password_hash)
            print("Password entered:", generate_password_hash(entered_password))

    return render_template('login.html', form=form, csrf_token=csrf_token)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm', validators=[DataRequired()])
    submit = SubmitField('Register')


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        email = form.email.data.lower()
        password = form.password.data
        confirm = form.password.data

        if password != confirm:
            flash('Passwords do not match', 'error')
            return redirect("/register")

        if not validate_password(password):
            flash('Password must contain letters, numbers, and symbols.', 'error')
            return redirect("/register")

        hash_password = generate_password_hash(password)

        if not db.execute("SELECT * FROM students WHERE email = ?", email):
            db.execute(
                "INSERT INTO students (email, password) VALUES (?, ?)", email, hash_password)
            flash('registration successful', 'success')
            return redirect("/login")
        else:
            flash('email already taken', 'error')
            return render_template('register.html', form=form)

    return render_template('register.html', form=form)


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


def validate_password(password):
    contains_letters = bool(re.search(r"[a-zA-Z]", password))
    contains_numbers = bool(re.search(r"\d", password))
    contains_symbols = bool(re.search(r"[^\w\s]", password))

    if contains_letters and contains_numbers and contains_symbols:
        return True
    else:
        return False


@app.route('/submit_recipe', methods=['GET', 'POST'])
@login_required
def submit_recipe():

    if request.method == 'POST':
        try:
            recipe_name = request.form.get('recipe_name').capitalize()
            author = request.form.get('author').capitalize()
            time = request.form.get('time')
            ingredients = request.form.getlist('ingredients[]')
            quantities = request.form.getlist('quantities[]')
            units = request.form.getlist('units[]')
            instructions = request.form.getlist('instructions[]')
            image_path = None

            if 'image' in request.files:
                image = request.files['image']
                if image.filename == '':
                    flash('No selected file')
                elif not allowed_file(image.filename):
                    flash(
                        'Invalid file extension. Please upload a file with one of the following extensions: png, jpg, jpeg, gif')
                else:
                    filename = secure_filename(image.filename)
                    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    image.save(image_path)

            author_id = session['student_id']
            conn = sqlite3.connect('hungrystudentss.db')

            cursor = conn.cursor()

            # Insert recipe into database
            cursor.execute("INSERT INTO recipes (recipe_name, author_id, time, image_path, author) VALUES (?, ?, ?, ?, ?)",
                        (recipe_name, author_id, time, image_path, author))

            # Fetch the last inserted row's ID
            recipe_id = cursor.lastrowid
            print("Last inserted recipe_id:", recipe_id)

            # Insert ingredients into database
            for ingredient, quantity, unit in zip(ingredients, quantities, units):

                if not quantity:
                    quantity = ''
                if not unit:
                    unit = ''
                cursor.execute("INSERT INTO ingredients (recipe_id, ingredient, quantity, unit) VALUES (?, ?, ?, ?)",
                            (recipe_id, ingredient, quantity, unit))

            # Insert instructions into database
            for step, instruction in enumerate(instructions, start=1):
                cursor.execute("INSERT INTO instructions (recipe_id, step, instruction) VALUES (?, ?, ?)",
                            (recipe_id, step, instruction))

            conn.commit()
            cursor.close()
            conn.close()

            flash('Recipe submitted successfully', 'success')
        except Exception as e:
            # Handle any errors
            flash('An error occurred while submitting the recipe. Please try again later.', 'error')
            print("Error occurred:", e)
            return render_template('submit_recipe.html', form={})

    return render_template('submit_recipe.html', form={})


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/my_recipe')
def my_recipe():
    if 'student_id' not in session:
        return redirect('/login')
    student_id = session['student_id']
    print("student in active session:", student_id)
    try:
        recipes = db.execute(
            "SELECT * FROM recipes WHERE author_id = ?", (student_id,))

        return render_template('my_recipe.html', recipes=recipes)

    except Exception as e:
        print("Error fetching recipes:", e)
        flash("You currently have no recipes", "success")
        return redirect('/submit_recipe')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/all_recipes')
def get_all_recipes():
    try:
        recipes = db.execute(
            "SELECT id, recipe_name, author, time, image_path FROM recipes")
        return jsonify(recipes)

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'Failed to fetch recipes'})

@app.route('/latest_recipes')
def get_latest_recipes():
    try:
        latest_recipes = db.execute(
            "SELECT id, recipe_name, author, time, image_path FROM recipes ORDER BY id DESC LIMIT 5")

        latest_recipes_list = [dict(row) for row in latest_recipes]

        return jsonify(latest_recipes_list)

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'Failed to fetch recipes'})


@app.route('/recipe-details/<int:recipe_id>', methods=['GET'])
def get_recipe_details(recipe_id):
    try:
        conn = sqlite3.connect('hungrystudentss.db')
        cursor = conn.cursor()

        # fetch the recipe details
        cursor.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
        recipes = cursor.fetchone()

        if recipes is None:
            abort(404)

        #fetch ingredients and instructions
        cursor.execute(
            "SELECT * FROM ingredients WHERE recipe_id = ?", (recipe_id,))
        ingredients = cursor.fetchall()

        cursor.execute(
            "SELECT * FROM instructions WHERE recipe_id = ?", (recipe_id,))
        instructions = cursor.fetchall()

        image_path_index = 5
        print("Image Path:", recipes[image_path_index])


        cursor.close()
        conn.close()

        return render_template('recipe-details.html', recipes=recipes, ingredients=ingredients, instructions=instructions)

    except sqlite3.Error as e:
        flash('An error occurred while fetching recipe details.', 'error')
        print("SQLite error:", e)
        abort(500)

    except Exception as e:
        flash('An unexpected error occurred.', 'error')
        print("Error:", e)
        abort(500)

if __name__ == '__main__':
    app.run(debug=True)
