from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')







#store pdfs in local mechine and in table just store the location of these pdfs. as pdfs are non structural dataset it is not recommended to store pdfs in tables.

if __name__ == '__main__':
    app.run(debug=True,port = 5001)
