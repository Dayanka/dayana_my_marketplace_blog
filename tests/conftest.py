import os
import sys
from dotenv import load_dotenv

load_dotenv()  # загрузит переменные из .env в окружение

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

#
# import pytest
# from app.db.base import Base
# from app.db.session import engine
#
# #сбрасываю бд с тестовыми данными, чтоб тесты не падали
# @pytest.fixture(autouse=True)
# def reset_database():
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)
#     yield