import validators


def check_url(url):
    if not validators.url(url):
        flash('Некорректный URL', 'error')
        if len(url) == 0:
            flash('URL обязателен', 'error')
    elif len(url) > 255:
        flash('URL превышает 255 символов', 'error')
    else:
        return False
    return True
