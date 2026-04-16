import sys
import os

from dns.asyncquery import udp

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from backend.models.database import Base, get_db
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from backend.models.user import User, Role
from backend.services.user_service import hash_password
from backend.models.task import Task


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base.metadata.create_all(bind=engine)


@pytest.fixture
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    return TestClient(app)



@pytest.fixture
def admin(db):
    user = User(
        name="admin",
        email="admin@test.com",
        password=hash_password("admin1234*"),
        role=Role.ADMIN.value
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def user(db):
    user = User(
        name="user",
        email="user@test.com",
        password=hash_password("user1234*"),
        role=Role.USER.value
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture(autouse=True)
def clean_db(db):
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(table.delete())
    db.commit()


@pytest.fixture
def task(db,user):
    task = Task(
        title= "test",
        description = "test task",
        priority= "LOW",
        status= "PENDING",
        user_id= user.user_id
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@pytest.fixture
def task_for_admin(db,admin):
    task = Task(
        title= "test",
        description = "test task",
        priority= "LOW",
        status= "PENDING",
        user_id= admin.user_id
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@pytest.fixture(autouse=True)
def disable_rate_limit():
    import backend.services.task_service as task_service
    task_service.check_rate_limit = lambda x: None