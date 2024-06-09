from flask import Flask, render_template, request, redirect, url_for, flash # NOQA E501
from datetime import date
from page_analyzer.validator import url_validator, url_normalize
import os
import requests
from page_analyzer.url_analyzer import url_analyze
from dotenv import load_dotenv
from page_analyzer.db import select_many_from_db, select_one_from_db, insert_into_db # NOQA E501
import psycopg2
from psycopg2 import pool # NOQA F401
from contextlib import contextmanager


load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
connect_db = psycopg2.pool.SimpleConnectionPool(1, 20, DATABASE_URL)  #check


@contextmanager
def get_connection():
    conn = None
    try:
        conn = connect_db.getconn()
        yield conn
        conn.commit()
    except Exception as error:
        conn.rollback()
        raise Exception(f'Connection lost. {error}')
    finally:
        if conn:
            connect_db.putconn(conn)


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def main_page():
    return render_template('index.html')


@app.route('/urls')
def list_page():
    with get_connection() as conn:
        requirement = '''
                SELECT urls.id, name, url_checks.created_at, status_code
                FROM urls LEFT JOIN url_checks ON urls.id = url_checks.url_id
                WHERE url_checks.id = (SELECT MAX(url_checks.id)
                FROM url_checks WHERE url_checks.url_id = urls.id)
                ORDER BY urls.id DESC'''
        data = select_many_from_db(conn, requirement, ())

    return render_template('list_of_urls.html', data=data)


@app.post('/urls')
def post_urls():
    URL = request.form['url']

    if not url_validator(URL):
        flash('Некорректный URL', category="danger")
        return render_template("index.html"), 422

    URL = url_normalize(URL)
    with get_connection() as conn:
        requirement = 'SELECT id FROM urls WHERE name = %s;'
        id = select_one_from_db(conn, requirement, (URL,))

    if id:
        flash('Страница уже существует', 'info')
        return redirect(url_for('link_page', id=id.id))

    with get_connection() as conn:
        requirement = 'INSERT INTO urls (name, created_at) VALUES (%s, %s);'
        insert_into_db(conn, requirement, (URL, date.today()))

        requirement = 'SELECT id FROM urls ORDER BY id DESC LIMIT 1;'
        id = select_one_from_db(conn, requirement, ()).id

    flash('Страница успешно добавлена', 'success') # NOQA E501
    return redirect(url_for('link_page', id=id))


@app.route('/urls/<id>')
def link_page(id):
    with get_connection() as conn:
        requirement = 'SELECT * FROM urls WHERE id = %s;'
        data_about_url = select_many_from_db(conn, requirement, (id,))

        requirement = '''SELECT id, status_code, h1, title, description,
                    created_at FROM url_checks WHERE url_id = %s
                    ORDER BY id DESC;'''
        data = select_many_from_db(conn, requirement, (id,))

    return render_template('link_page.html',
                           data_about_url=data_about_url,
                           id=id,
                           data=data)


@app.post('/urls/<id>/check')
def url_check(id):
    with get_connection() as conn:
        requirement = 'SELECT name FROM urls WHERE id = %s;'
        name = select_one_from_db(conn, requirement, (id,)).name

    request = requests.get(name)

    if request.status_code == 200:
        flash('Страница успешно проверена', 'success') # NOQA E501
        status_code, h1, title, description = url_analyze(name)
        with get_connection() as conn:
            requirement = '''INSERT INTO url_checks (url_id,
                status_code, h1, title, description,
                created_at) VALUES (%s, %s, %s, %s, %s, %s)'''
            insert_into_db(
                conn,
                requirement,
                (id, status_code, h1, title,
                 description, date.today()))

        return redirect(url_for('link_page', id=id))
    else:
        flash('Произошла ошибка при проверке', 'danger') # NOQA E501
        return redirect(url_for('link_page', id=id))


@app.errorhandler(404)
def error_page(e):
    return render_template("error_page.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
