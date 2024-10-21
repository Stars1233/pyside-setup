# Copyright (C) 2024 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import platform
from pathlib import Path

Base = declarative_base()


class Finance(Base):
    __tablename__ = 'finances'
    id = Column(Integer, primary_key=True)
    item_name = Column(String)
    category = Column(String)
    cost = Column(Float)
    date = Column(String)


# Check for an environment variable for the database path
env_db_path = os.getenv('FINANCE_MANAGER_DB_PATH')

if env_db_path:
    db_path = Path(env_db_path)
else:
    # Determine the application data directory based on the operating system using pathlib
    if platform.system() == 'Windows':
        app_data_location = Path(os.getenv('APPDATA')) / 'FinanceManager'
    elif platform.system() == 'Darwin':  # macOS
        app_data_location = Path.home() / 'Library' / 'Application Support' / 'FinanceManager'
    else:  # Linux and other Unix-like systems
        app_data_location = Path.home() / '.local' / 'share' / 'FinanceManager'

    db_path = app_data_location / 'finances.db'

DATABASE_URL = f'sqlite:///{db_path}'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Default data to be added to the database
default_data = [
    {"item_name": "Mobile Prepaid", "category": "Electronics", "cost": 20.00, "date": "15-02-2024"},
    {"item_name": "Groceries-Feb-Week1", "category": "Groceries", "cost": 60.75,
     "date": "16-01-2024"},
    {"item_name": "Bus Ticket", "category": "Transport", "cost": 5.50, "date": "17-01-2024"},
    {"item_name": "Book", "category": "Education", "cost": 25.00, "date": "18-01-2024"},
]


def initialize_database():
    if db_path.exists():
        print(f"Database '{db_path}' already exists.")
        return

    app_data_location.mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(engine)
    print(f"Database '{db_path}' created successfully.")
    session = Session()

    for data in default_data:
        finance = Finance(**data)
        session.add(finance)

    session.commit()
    print("Default data has been added to the database.")
