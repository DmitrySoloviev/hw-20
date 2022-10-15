from dao.genre import GenreDAO
import pytest
from unittest.mock import MagicMock
from service.genre import GenreService
from dao.model.genre import Genre
from setup_db import db


@pytest.fixture()
def genre_dao():
    genre_dao = GenreDAO(db.session)

    g1 = Genre(id=1, name='comedy')
    g2 = Genre(id=2, name='drama')
    d3 = Genre(id=3, name='doc')

    genre_dao.get_one = MagicMock(return_value=Genre(id=1))
    genre_dao.get_all = MagicMock(return_value=['comedy', 'drama', 'doc'])
    genre_dao.create = MagicMock(return_value=Genre(id=3))
    genre_dao.delete = MagicMock()
    genre_dao.update = MagicMock()
    return genre_dao



class TestGenreService:
    @pytest.fixture(autouse=True)
    def genre_service(self, genre_dao):
        self.genre_service = GenreService(dao=genre_dao)

    def test_get_one(self):
        genre = self.genre_service.get_one(1)
        assert genre is not None
        assert genre.id is not None


    def test_get_all(self):
        genres = self.genre_service.get_all()
        assert len(genres) > 0

    def test_create(self):
        director_new = {
            "name": "action"
        }
        genre = self.genre_service.create(director_new)
        assert genre.id is not None

    def test_update(self):
        genre_new = {
            "id": 3,
            "name": "Historical",
        }
        self.genre_service.update(genre_new)

    def test_delete(self):
        self.genre_service.delete(1)

