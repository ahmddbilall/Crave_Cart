from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy.orm import sessionmaker
from DataBase import User

app = Flask(__name__)

session = sessionmaker()



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if session.query(User).filter_by(email=email).first():
            return render_template('signup.html', message='Email already exists. Please choose a different email.')
        
        new_user = User(username=username, email=email, password=password)
        session.add(new_user)
        session.commit()
        
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = session.query(User).filter_by(email=email, password=password).first()
        if user:
            return redirect(url_for('/'))
        else:
            return render_template('login.html', message='Invalid email or password. Please try again.')

    return render_template('login.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')


@app.route('/book')
def book():
    return render_template('book.html')


if __name__ == '__main__':
    app.run(debug=True,port = 5001)
