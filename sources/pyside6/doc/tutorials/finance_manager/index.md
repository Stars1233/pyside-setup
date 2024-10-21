(tutorial_financemanager)=

# Finance Manager Tutorial

## Summary

This tutorial series is structured into three comprehensive parts, each building upon the previous
one to create a fully functional finance manager application. It demonstrates how PySide6 can be
used to interact with other popular packages in the Python ecosystem. The series starts with the
basics of PySide6 and QtQuick, then integrates SQLite for database management using
[SQLAlchemy], and finally incorporates [FastAPI] and [Pydantic] for server-side operations and
REST API integration.


### Part 1: Building a Complete PySide6 QtQuick Application
- **Introduction**: Overview of the tutorial series and prerequisites.
- **Project Setup**: Setting up the development environment and installing necessary packages.
- **Creating the Main Window**: Setting up the main window using PySide6 and
    creating the main QML file.
- **Adding Basic UI Components**: Adding buttons, labels, input fields, listview, Pie chart and
    handling user interactions with PySide6 and QML.
- For more details, see {ref}`tutorial_financemanager_partone`.

### Part 2: Integrating SQLite Database with SQLAlchemy
- **Setting Up SQLAlchemy**: Installing SQLAlchemy and configuring the SQLite database connection.
- **Creating Database Models**: Defining database models for finance data.
- **CRUD Operations**: Implementing part of the CRUD operations through Create, and Read operations
  and connecting them to the PySide6 application.

### Part 3: Using FastAPI and Pydantic for Server-Side Operations
- **Setting Up FastAPI**: Installing FastAPI and Uvicorn, and creating a basic FastAPI application.
- **Creating REST Endpoints**: Defining RESTful endpoints for finance data and implementing CRUD
  operations through the API.
- **Connecting FastAPI with PySide6**: Making HTTP requests from the PySide6 application and
  displaying data fetched from the API in the UI.

Each parts ends with instruction on how to deploy the application using {ref}`pyside6-deploy`.
This structured approach ensures that readers can follow along and understand each concept before
moving on to the next one, resulting in a robust and scalable finance manager application.

[SQLalchemy]: https://www.sqlalchemy.org/
[FastApi]: https://fastapi.tiangolo.com/
[PyDantic]: https://pydantic-docs.helpmanual.io/

```{toctree}
:maxdepth: 1
:hidden:

part1/part1.md
