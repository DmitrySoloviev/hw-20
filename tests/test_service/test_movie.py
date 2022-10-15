from dao.movie import MovieDAO
import pytest
from unittest.mock import MagicMock
from service.movie import MovieService
from dao.model.genre import Genre
from dao.model.director import Director
from dao.model.movie import Movie
from setup_db import db


@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(db.session)

    m1 = Movie(id=1, title="Movie_1", description="description_1", trailer="trailer_1",
               year=2001, rating=1.0, genre_id=1, genre={}, director_id=1, director={})
    m2 = Movie(id=2, title="Movie_2", description="description_2", trailer="trailer_2",
               year=2002, rating=2.0, genre_id=1, genre={}, director_id=1, director={})
    m3 = Movie(id=3, title="Movie_3", description="description_3", trailer="trailer_3",
               year=2002, rating=2.0, genre_id=1, genre={}, director_id=1, director={})

    movie_dao.get_one = MagicMock(return_value=Movie(id=1))
    movie_dao.get_all = MagicMock(return_value=[("Movie_1", "description_1", "trailer_1", 2001,
                                  1.0, 1, 1), ("Movie_2", "description_2", "trailer_2", 2002,
                                  2.0, 1, {}, 1, {}), ("Movie_3", "description_3", "trailer_3", 2002,
                                  2.0, 1, {}, 1, {})])
    movie_dao.create = MagicMock(return_value=Movie(id=3))
    movie_dao.delete = MagicMock()
    movie_dao.update = MagicMock()
    return movie_dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)
        assert movie is not None
        assert movie.id is not None

    def test_get_all(self):
        movies = self.movie_service.get_all()
        assert len(movies) > 0

    def test_create(self):
        movie_new = {
            'title': 'Movie_4',
            'description': 'description_4',
            'trailer': "trailer_4",
            'year': 2005,
            'rating': 3.0,
            'genre_id': 1,
            'genre': {},
            'director_id': 2,
            'director': {}
        }
        movie = self.movie_service.create(movie_new)
        assert movie.id is not None

    def test_update(self):
        movie_new = {
            'id': 3,
            'title': 'Movie_3',
            'description': 'description_3',
            'trailer': "trailer_3",
            'year': 2005,
            'rating': 5.0,
            'genre_id': 1,
            'genre': {},
            'director_id': 2,
            'director': {}
        }
        self.movie_service.update(movie_new)

    def test_delete(self):
        self.movie_service.delete(1)

