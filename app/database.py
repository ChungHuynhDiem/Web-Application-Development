# test_create_db.py
from app import app, db  # thay your_app_file bằng tên file thật, không có .py
with app.app_context():
    db.create_all()
    print("Database created!")
