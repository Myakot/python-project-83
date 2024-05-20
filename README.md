# Page analyzer

### Hexlet tests and linter status:
[![Actions Status](https://github.com/Myakot/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Myakot/python-project-83/actions)
[![Actions Status](https://github.com/Myakot/python-project-83/workflows/hexlet-check/badge.svg)](https://github.com/Myakot/python-project-83/actions)
[![Actions Status](https://github.com/Myakot/python-project-83/workflows/flake8/badge.svg)](https://github.com/Myakot/python-project-83/actions/workflows/flake8.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/98a86e836514fd92d4f8/maintainability)](https://codeclimate.com/github/Myakot/python-project-83/maintainability)

### Description
Page Analyzer is a site that analyzes websites for SEO suitability.  
The application uses Python library 
[Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) to parse websites.  
The results of the checks of websites are parsing: 
h1, title, description and code status.
The application saves all of it on a remote postgres database.

### Demonstration

The production version of the app is (hopefully) available at the following URL:
[Page analyzer](https://python-project-83-daxw.onrender.com)

### Running the project:
```
$ git clone git@github.com:Myakot/python-project-83.git  
$ cd python-project-83  
$ make install  
```

Make sure you have python3, pip3 and postgres installed.
Create a ".env" file in the project folder, add these variables into it:
```  
SECRET_KEY={secret_key}  
DATABASE_URL=postgresql://{user_name}:{password}@localhost:5432/page_analyzer  
```  
In order to get your own database credentials, sign up on [Postgres](https://www.postgresql.org/) 
or [Render](https://render.com/)

After everything is setup just type `make run` to start the project.

### Recorded example run:
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/kIrgt-7IFp0/0.jpg)](https://www.youtube.com/watch?v=kIrgt-7IFp0)

### Tools used during the making of this project:
```
python = "^3.10"
urllib3 = "1.26.15"
Flask = "^3.0.3"
gunicorn = "^22.0.0"
psycopg = "^3.1.18"
requests = "^2.31.0"
psycopg2-binary = "^2.9.9"
python-dotenv = "^1.0.1"
validators = "^0.28.1"
bs4 = "^0.0.2"
```