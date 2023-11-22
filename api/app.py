#!usr/bin/python3
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import check_password_hash, Bcrypt, generate_password_hash
import requests
import json
from models import db, User, Question, Options, Quiz

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://quizify:quizify_pwd@localhost/quiz_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # To suppress a warning

migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
bcrypt = Bcrypt()
db.init_app(app)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if the username is already taken
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already taken. Please choose another.', 'danger')
            return redirect(url_for('register'))

        # Hash the password before storing it in the database
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create a new user instance
        new_user = User(username=username, password=hashed_password)

        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully. You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(int(user_id))

# Rest of your routes and logic...
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Check your username and password.', 'danger')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    quizzes = Quiz.query.all()
    return render_template('dashboard.html', quizzes=quizzes)

@app.route('/quiz/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)

    if not quiz:
        flash('Quiz not found.', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        score = 0

        for question in quiz.questions:
            user_answer = request.form.get(f'question_{question.id}')
            correct_option = Options.query.filter_by(question_id=question.id, is_correct=True).first()

            if user_answer and user_answer == str(correct_option.id):
                score += 1

        flash(f'Quiz completed! Your score: {score}/{len(quiz.questions)}', 'success')
        return redirect(url_for('dashboard'))

    return render_template('quiz.html', quiz=quiz)


@app.route('/create_quiz_from_api')
@login_required
def create_quiz_from_api():
    # Make a request to the API to fetch quiz data
    api_url = 'https://opentdb.com/api.php?amount=30&category=9&difficulty=medium&type=multiple'
    response = requests.get(api_url)

    if response.status_code == 200:
        quiz_data = response.json()

        # Create a new quiz instance
        new_quiz = Quiz(title='Quiz from API')
        db.session.add(new_quiz)
        db.session.commit()

        # Parse the API data and create questions and options
        for result in quiz_data['results']:
            question_text = result['question']
            correct_option_text = result['correct_answer']
            incorrect_options = result['incorrect_answers']

            # Create a new question for the quiz
            new_question = Question(text=question_text, quiz=new_quiz)
            db.session.add(new_question)
            db.session.commit()

            # Create options for the question
            correct_option = Options(text=correct_option_text, is_correct=True, question=new_question)
            db.session.add(correct_option)
            db.session.commit()

            for incorrect_option_text in incorrect_options:
                incorrect_option = Options(text=incorrect_option_text, is_correct=False, question=new_question)
                db.session.add(incorrect_option)
                db.session.commit()

        flash('Quiz created successfully from API!', 'success')
    else:
        flash('Failed to fetch quiz data from API.', 'danger')

    return redirect(url_for('dashboard'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)