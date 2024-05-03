from flask import (Flask, render_template, request, redirect,
                   url_for, flash, get_flashed_messages)
from dotenv import load_dotenv
import os
from .database_manager import DbManager


load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


db = DbManager()


@app.route('/', methods=['GET'])
def start_page():
    messages = get_flashed_messages(with_categories=True)
    return render_template('main.html', messages=messages)