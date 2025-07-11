from typing import Union

from fastapi import FastAPI, Depends
from typing import Annotated

from routes import pdf_route, query_route

# from database import create_db_and_tables

# import models


# create_db_and_tables()
app = FastAPI()

app.include_router(pdf_route.router)
app.include_router(query_route.router)
