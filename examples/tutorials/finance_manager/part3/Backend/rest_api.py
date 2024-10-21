# Copyright (C) 2024 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

import logging
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from sqlalchemy import orm
from database import Session, Finance

app = FastAPI()


class FinanceCreate(BaseModel):
    item_name: str
    category: str
    cost: float
    date: str


class FinanceRead(FinanceCreate):
    class Config:
        from_attributes = True


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


@app.post("/finances/", response_model=FinanceRead)
def create_finance(finance: FinanceCreate, db: orm.Session = Depends(get_db)):
    print(f"Adding finance item: {finance}")
    db_finance = Finance(**finance.model_dump())
    db.add(db_finance)
    db.commit()
    db.refresh(db_finance)
    return db_finance


@app.get("/finances/", response_model=Dict[str, Any])
def read_finances(skip: int = 0, limit: int = 10, db: orm.Session = Depends(get_db)):
    try:
        total = db.query(Finance).count()
        finances = db.query(Finance).offset(skip).limit(limit).all()
        response = {
            "total": total,
            # Convert the list of Finance objects to a list of FinanceRead objects
            "items": [FinanceRead.from_orm(finance) for finance in finances]
        }
        logging.info(f"Response: {response}")
        return response
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
