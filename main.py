from flask import Flask, render_template

app = Flask(__name__)











@app.route('/')
def home():
    return render_template('index.html')



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
