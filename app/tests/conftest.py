from datetime import datetime
import pytest
from flask import template_rendered
from contextlib import contextmanager
# from app import app as application
from app.app import app as application

# # from app.app import create_app  # Import hàm khởi tạo app


# @pytest.fixture
# def app():
#     return application

# @pytest.fixture
# def client(app):
#     return app.test_client()

# @pytest.fixture
# @contextmanager
# def captured_templates(app):
#     recorded = []
#     def record(sender, template, context, **extra):
#         recorded.append((template, context))
#     template_rendered.connect(record, app)
#     try:
#         yield recorded
#     finally:
#         template_rendered.disconnect(record, app)

# @pytest.fixture
# def posts_list():
#     return [
#         {
#             'title': 'Заголовок поста',
#             'text': 'Текст поста',
#             'author': 'Иванов Иван Иванович',
#             'date': datetime(2025, 3, 10),
#             'image_id': '123.jpg',
#             'comments': [],
#             'avatarclient': 'client.jpg',
#         }
#     ]

import pytest
from app.app import app, db, User
from flask import url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import database


@pytest.fixture
def app():
    return application

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Tạo user test
            hashed_pw = generate_password_hash('testpass')
            test_user = User(
                UserName='testuser',
                PassWord=hashed_pw,
                FullName='Test User',
                UserRole='user'
            )
            db.session.add(test_user)
            db.session.commit()
        yield client
