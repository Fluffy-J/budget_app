# Django Budget Application. 

A Django-based budgeting application with a server-rendered web interface and REST API.

**Live Demo: ** %place deployed application link here%

## Table of Contents

* [About the Project](#about-the-project)
* [Built With](#built-with)
* [Getting Started](#getting-started)
* [Usage](#usage)
* [Screenshots](#screenshots)
* [API Endpoints](#api-endpoints)
* [Testing](#testing)
* [Deployment](#deployment)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [Contact](#contact)

## About the Project

The Django Budget Application is a practical backend-focused project displaying, REST API development, relational data modelling, automated testing, and production deployment.

The application allows users to:

* Create a budget plan 
* View all budgets plans created 
* Delete a budget plan 
* Interact with a budget plan through a REST API

The project uses SQLite for local development and production.

### Why I Built It

The project is as a solution to a reckless habit of poor financial management. 

During development, the application was strengthened through:

* REST API development
* Production configuration
* Static-file handling
* Automated testing
* Cloud deployment
* Authetication
* UUID intergration

## Built With

* **Python 3.11**
* **Django 5.2.17**
* **Django REST Framework 3.18.0**
* **SQLite** — local development
* **WhiteNoise** — static files
* **Gunicorn + Uvicorn** — production server
* **Pipenv** — dependency management
* **Render** — deployment

## Getting Started

### Prerequisites

You will need:

* Python 3.11
* Pip
* Pipenv
* Git

### Installation

Clone the repository:

```bash
git clone %add https link here%
cd budget_app
```

Install dependencies:

```bash
pip install pipenv
pipenv sync
```

Create a `.env` file in the project root:

```env
DJANGO_SECRET_KEY
```

Apply the database migrations:

```bash
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

Open:

```text
%place the URL link here %
```

## Usage



% Insert image here and description %

The application also exposes a REST API for programmatic interaction with the budget.

## Screenshots

### Application Interface

% Insert image here and description %

### Create A Budget Plan

% Insert image here and description %

### API

% Insert image here and description %


### Production Deployment

% Insert image here and description %


## API Endpoints

% Insert endpoints here %

Example request:

% Insert example endpoint here %
```

## Testing

The project uses Django's testing framework and Django REST Framework's `APITestCase`.

Tests are separated by responsibility:

```text
notes/tests/
├── test_models.py
├── test_views.py
└── test_api.py
```

The current test suite contains ** xxxx automated tests** covering:

* Model behaviour and relationships
* Web views
* Note creation and deletion
* REST API operations
* Database changes
* Regression cases

Run the complete test suite with:

```bash
python manage.py test notes
```

% Insert image of output of tests here %

## Deployment

The application is deployed on Render.

% Insert render url here %

Production uses:

* Gunicorn
* Uvicorn
* WhiteNoise
* Environment-based configuration

The deployment process installs the locked dependencies, collects static files, and applies database migrations.

% Insert image of application starting up on render %

## Contributing

This project is a portfolio project, but suggestions and improvements are welcome.

To contribute:

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Run the test suite.
5. Submit a pull request.

## Contact

**Fluffy-J**

GitHub: https://github.com/Fluffy-J

Project Repository: https://github.com/Fluffy-J/django_notesapp

Live Application: % Insert render URL %
