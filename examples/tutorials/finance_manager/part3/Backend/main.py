# Copyright (C) 2024 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

import uvicorn
from database import initialize_database


def main():
    # Initialize the database
    initialize_database()
    # Start the FastAPI endpoint
    uvicorn.run("rest_api:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
