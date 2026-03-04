from backend.controllers import user_controller as user_controller
from backend.controllers import task_controller as task_controller
from backend.models.database import Base, engine
from fastapi import FastAPI

app = FastAPI()

app.include_router(user_controller.api)
app.include_router(task_controller.api)

Base.metadata.create_all(engine)  # This is to create models in the database



# To generate a SECRET_KEY for token
# import os
# print(os.urandom(32).hex())  # I put the result in .env file


