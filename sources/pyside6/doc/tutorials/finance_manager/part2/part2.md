(tutorial_financemanager_parttwo)=

# Finance Manager Tutorial - Part 2

In this part of the tutorial, we will extend our finance manager app to store the expenses in a
SQLite database using the [SQLAlchemy] Python package. This will allow us to
persist the data and retrieve it even after the application is closed.

To download the complete source code for this tutorial, visit
{ref}`example_tutorials_finance_manager_part2`.

## Prerequisites

Before we begin, make sure you have [SQLAlchemy] installed within your Python environment.

You can install it using pip:

```bash
pip install sqlalchemy
```

## Project Structure

The overall project structure is the same as in the [previous part](tutorial_financemanager_partone)
of the tutorial.

## Let's Get Started!

### Creating the Database

The first step is to create a `database.py` that takes care of creating and initializing the
database. This Python code will define the database schema and provide a session object to interact
with the database. The database is initialized with a single table named `finances` with the same
initial data we used in the [part one](tutorial_financemanager_partone) of the tutorial.

<details>
<summary class="prominent-summary">database.py</summary>

```{literalinclude} ../../../../../../../../../examples/tutorials/finance_manager/part2/database.py
---
language: python
caption: database.py
linenos: true
---
```
</details>

> Note: The database called `finances.db` will be created in the directory specified by the
`FINANCE_MANAGER_DB_PATH` environment variable if it is set. If the environment variable is not set,
the database will be created in the appropriate application data directory based on the operating
system.

### Updating the FinanceModel Class

Next, we need to update the FinanceModel class to interact with the database.

In `financemodel.py`, make the following highlighted changes to load the existing expenses from the
database into the model, and also save new expenses to the database.

<details>
<summary class="prominent-summary">financemodel.py</summary>

```{literalinclude} ../../../../../../../../../examples/tutorials/finance_manager/part2/financemodel.py
---
language: python
caption: Finance model class definition
linenos: true
emphasize-lines: 12, 40-50, 93-101
---
```

## Updating the Main Application

Finally, we need to update the `main.py` file to initialize the database and use the `FinanceModel`

<details>
<summary class="prominent-summary">main.py</summary>

```{literalinclude} ../../../../../../../../../examples/tutorials/finance_manager/part2/main.py
---
language: python
caption: main.py
linenos: true
emphasize-lines: 11, 15
---
```
</details>

The rest of the code remains the same as in the previous part of the tutorial.

### Running the Application

To run the application, execute the `main.py` file using Python:

```bash
python main.py
```

### Deploying the Application

To deploy the application, follow the same steps as in the
[previous part](tutorial_financemanager_partone) of the tutorial.

## Summary

In this part of the tutorial, we have extended the finance manager app by integrating a database
using [SQLAlchemy]. This allows us to store the expenses and retrieve them even after the
application is closed.

In the next part of the tutorial, we will continue to enhance the application by using
[FastApi] and [PyDantic] to create a REST API for the finance manager app, and move the
database to a separate server.

[SQLalchemy]: https://www.sqlalchemy.org/
[FastApi]: https://fastapi.tiangolo.com/
[PyDantic]: https://pydantic-docs.helpmanual.io/
