from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    get_flashed_messages,
    url_for
)
import os
import datetime
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import page_analyzer.db as db
from .utils import check_url


try:
    from dotenv import load_dotenv
    load_dotenv()
except ModuleNotFoundError:
    pass

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', messages=messages)


@app.post('/urls')
def post_urls():
    url = request.form.get('url')
    if check_url(url):
        messages = get_flashed_messages(with_categories=True)
        return render_template('index.html', messages=messages), 422
    url = urlparse(url)
    url = f'{url.scheme}://{url.netloc}'
    id = db.add_url_to_database(url)
    if id is not None:
        flash('Страница уже существует', 'warning')
        return redirect(url_for('get_url_by_id', id=id[0]))
    flash('Страница успешно добавлена', category='success')
    id = db.insert_url(url, datetime.date.today())
    return redirect(url_for('get_url_by_id', id=id.id))


@app.get('/urls')
def get_all_urls():
    urls = db.get_all_urls()
    return render_template('urls/list.html', urls=urls)


@app.get('/urls/<int:id>')
def get_url_by_id(id):
    message = get_flashed_messages(with_categories=True)
    url = db.select_url_by_id(id)
    checks = db.get_url_checks(id)
    return render_template(
        'urls/detail.html',
        url=url.name,
        id=id,
        created_at=url.created_at,
        messages=message,
        checks=checks
    )


@app.post('/urls/<int:id>/checks')
def post_check_id(id):
    url = db.select_url_by_id(id)
    try:
        response = requests.get(url.name)
        if response.status_code != 200:
            raise requests.RequestException
        status = response.status_code
        html_data = response.content
        soap = BeautifulSoup(html_data, 'html.parser')
        title = soap.title.text if soap.title is not None else ''
        h1 = soap.h1.text if soap.h1 is not None else ''
        content = soap.find('meta', {"name": "description"})
        content = content.attrs['content'] if content else ''
        flash('Страница успешно проверена', 'success')
        db.add_url_checks(
            id,
            status,
            h1,
            title,
            content,
            datetime.date.today()
        )
    except requests.RequestException:
        flash('Произошла ошибка при проверке', 'error')
    return redirect(url_for('get_url_by_id', id=id))


if __name__ == '__main__':
    app.run()
