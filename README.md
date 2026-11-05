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

The application provides a browser interface for managing notes.

<img width="1720" height="877" alt="image" src="https://github.com/user-attachments/assets/10d34492-1f1a-41c8-9ede-5364475873da" />

Users can create a note containing a title and body, view individual notes, and delete notes.

The application also exposes a REST API for programmatic interaction with the notes.

## Screenshots

### Application Interface

<img width="1333" height="2000" alt="interface" src="https://github.com/user-attachments/assets/6b8a52c4-1545-4c13-af5c-119c25a5703f" />

### Create Note

<img width="1596" height="872" alt="image" src="https://github.com/user-attachments/assets/b681a031-ce84-442b-aab3-6999796b178c" />

### API

<img width="1068" height="667" alt="image" src="https://github.com/user-attachments/assets/fee8c333-e0b8-46a6-9202-07592f24dbb2" />


### Production Deployment

<img width="807" height="815" alt="image" src="https://github.com/user-attachments/assets/4eec1492-a701-440b-a3db-48d6e5e8170b" />


## API Endpoints

| Method | Endpoint                | Description         |
| ------ | ----------------------- | ------------------- |
| GET    | `/api/log/`             | List notes          |
| POST   | `/api/makenote/`        | Create a note       |
| PUT    | `/api/updatenote/<id>/` | Update a note title |
| DELETE | `/api/noteDelete/<id>/` | Delete a note       |

Example request:

```/api/makenote/

{
  "title": "Test_5",
  "body_text": "Created through the production API"
}

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

The current test suite contains **14 automated tests** covering:

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

<img width="970" height="240" alt="image" src="https://github.com/user-attachments/assets/0b5437d1-0402-44cd-a51d-bd9dfdde3398" />

## Deployment

The application is deployed on Render.

**Live application:** https://notesapp-qv1o.onrender.com

Production uses:

* PostgreSQL
* Gunicorn
* Uvicorn
* WhiteNoise
* Environment-based configuration

The deployment process installs the locked dependencies, collects static files, and applies database migrations.

<img width="807" height="815" alt="image" src="https://github.com/user-attachments/assets/36445f4c-e3d5-4e9f-a709-c9b0210d0f2c" />

## Roadmap

Planned improvements include:

* User authentication
* User-specific note ownership
* API permissions
* Improved API validation
* Editing note bodies through the API
* Pagination
* Continuous integration
* Improved frontend styling

## Contributing

This project is primarily a portfolio project, but suggestions and improvements are welcome.

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

Live Application: https://notesapp-qv1o.onrender.com
