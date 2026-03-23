from backend.controllers import user_controller, health
from backend.controllers import task_controller
from backend.controllers import logged_controller
from backend.models import database as database
from backend.models.database import Base, engine
from backend.models.user import User
from backend.models.task import Task
from backend.models.logged import Logged
from fastapi import FastAPI


app = FastAPI()

app.include_router(user_controller.api)
app.include_router(task_controller.api)
app.include_router(logged_controller.api)
app.include_router(health.api)

Base.metadata.create_all(engine)  # This is to create models in the database


# To generate a SECRET_KEY for token
# import os
# print(os.urandom(32).hex())  # I put the result in .env file


