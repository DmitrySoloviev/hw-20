from dao.director import DirectorDAO
import pytest
from unittest.mock import MagicMock
from service.director import DirectorService
from dao.model.director import Director
from setup_db import db


@pytest.fixture()
def director_dao():
    director_dao = DirectorDAO(db.session)

    d1 = Director(id=1, name='ivan')
    d2 = Director(id=2, name='oleg')
    d3 = Director(id=3, name='vadim')

    director_dao.get_one = MagicMock(return_value=Director(id=1))
    director_dao.get_all = MagicMock(return_value=['ivan', 'oleg', 'vadim'])
    director_dao.create = MagicMock(return_value=Director(id=3))
    director_dao.delete = MagicMock()
    director_dao.update = MagicMock()
    return director_dao


class TestDirectorService:
    @pytest.fixture(autouse=True)
    def director_service(self, director_dao):
        self.director_service = DirectorService(dao=director_dao)

    def test_get_one(self):
        director = self.director_service.get_one(1)
        assert director is not None
        assert director.id is not None

    def test_get_all(self):
        directors = self.director_service.get_all()
        assert len(directors) > 0

    def test_create(self):
        director_new = {
            "name": "Polina"
        }
        director = self.director_service.create(director_new)
        assert director.id is not None

    def test_update(self):
        director_new = {
            "id": 3,
            "name": "John",
        }
        self.director_service.update(director_new)

    def test_partially_update(self):
        director_d = {
            "id": 3,
            "name": "Sergey"
        }
        self.director_service.partially_update(director_d)

    def test_delete(self):
        self.director_service.delete(1)

