from flask import Flask, render_template
from flask import get_flashed_messages


app = Flask(__name__)
app.secret_key = 'secret key'


@app.route('/')
def index():
    messages = get_flashed_messages(with_categories=True)
    return render_template("main.html", messages=messages)