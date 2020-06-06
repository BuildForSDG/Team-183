# Team-183-Backend

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/6c9d7de398b64a68bf8446209a78f342)](https://app.codacy.com/gh/BuildForSDG/Team-183-Backend?utm_source=github.com&utm_medium=referral&utm_content=BuildForSDG/Team-183-Backend&utm_campaign=Badge_Grade_Settings)

## About

What is this project about. Ok to enrich here or the section above it with an image.
The project is about promoting chicken farming with the sustainable development goal(SDG) of ending hunger by 2030 globally.


This is a simple python starter repo template for setting up your project. The setup contains:

-   install: poetry via pip. poetry is a dependecy manager.
-   poetry: configuration in pyproject.toml
-   flake8: for linting and formatting

## Why

The problem this solves, SDG(s) and SGD targets it addresses and why these are important
This application has the goal of solving the SDG problem of Hunger with a target to end hunger and malnutrition by 2030 through deliberate and well calculated promotion of chicken farming that is not only an affordable investment but easy to adopt and practice widely.
Our aim is to encourage chicken farming by connecting these chicken farmers to vendor-markets who are either individual vendors, consumers or resturants.
These platform also has an additional interractive features where different types of users would come together and blog for instance the consumers who would likely blog on their favorite chicken recipes. Separately vendors would blog about areas of interest to them like rating and analyzing the supply chains.

## API Usage

How would someone use what you have built, include URLs to the deployed app, service e.t.c when you have it setup

### Auth Endpoints Version 1

| **EndPoint**                         | **Functionality**    |
| ------------------------------------ | -------------------- |
| POST `/api/v1/users/signup`          | Register a user      |
| POST `/api/v1/users/login`           | Logs in a user       |
| POST `/api/v1/users/forgot-password` | User forgot password |
| POST `/api/v1/users/reset-password`  | User reset password  |

## Setup

You should have **Python 3.5+** and **git** installed.

1.  Clone the repo you've created from the template herein and change into the directory

    `git clone https://github.com/BuildForSDG/Team-183-Backend.git

2.  Change into repo directory

    `cd Team-183-Backend`

3.  Install poetry, a dependecy manager for python.

    On windows, you will need powershell to install it:

    `(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python`

    After that you will need to restart the shell to make it operational.

    On linux and other posix systems (mac included):

    `curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python`

    To check that it is correctly installed, you can check the version:
    `poetry --version`

    May be the latest stable version is not installed with the installation script, to update poetry, you can run:

    `poetry self update`

4.  With poetry installed, you should install project dependecies by running:

    `poetry install` or `pip install -r requirements.txt`

    This will install pytest for running tests and flake8, linter for your project.

### To Note

`src/app.py` is the entry to the project and source code should go into the `src` folder.

All tests should be written in the `tests` folder. tests/test_src.py is a sample test file that shows how tests should like. Feel free to delete it.

#### Hints

-   Lint: `poetry run flake8`

-   Run tests using the command: `poetry run pytest`

-   Install dependencies:
    `poetry add <dependency>`

-   Install dev dependencies:
    `poetry add --dev <dev-dependency>`

-   Run your project:
    `poetry run app` or `python manage.py runserver`

Set environment variables for in the format proscribed in the `.env.example` file

> `JWT_SECRET_KEY` is your secret key
> `FLASK_ENV` is the enviroment you are running on. Should be either `Production`, `Development` or `Testing`. NOTE: its case sensitive

> `GMAIL_MAIL` > `GMAIL_USERNAME` > `GMAIL_PASSWORD` > `MAIL_SERVER` > `MAIL_PORT` > `MAIL_USE_TLS`

> `MONGO_URI` which is in uri format on localhost is `'mongodb://localhost:27017/reactloginreg'`
> for `MONGO_URI_TEST` or `MONGO_URI_DEV` or `MONGO_URI_PROD`

> `MONGO_DBNAME` the name of the app database

## API Documentation

Once app server is running you can view API documentation locally from

```
http://localhost:5000/
```

_VERSION 1_ on HEROKU the [API documentation here](https://chicken-farm-ke.herokuapp.com/)

## Authors

1\. Daniel Kamar - Team Lead <https://github.com/koitoror>.  
2\. Osumgba Chiamaka - Mentor <https://github.com/osumgbachiamaka>.  
3\. Adele Gikonyo - <https://github.com/adelewg>.  
4\. Salma - Team Coordinator. <https://github.com/SalmaQueen>.

## Contributing

If this project sounds interesting to you and you'd like to contribute, thank you!
First, you can send a mail to buildforsdg@andela.com to indicate your interest, why you'd like to support and what forms of support you can bring to the table, but here are areas we think we'd need the most help in this project :

1.  area one (e.g this app is about human trafficking and you need feedback on your roadmap and feature list from the private sector / NGOs)
2.  area two (e.g you want people to opt-in and try using your staging app at staging.project-name.com and report any bugs via a form)
3.  area three (e.g here is the zoom link to our end-of sprint webinar, join and provide feedback as a stakeholder if you can)

## Acknowledgements

Did you use someone else’s code?
Do you want to thank someone explicitly?
Did someone’s blog post spark off a wonderful idea or give you a solution to nagging problem?

It's powerful to always give credit.

## LICENSE

MIT
