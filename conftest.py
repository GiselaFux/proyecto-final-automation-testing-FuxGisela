import pytest

from pages.posts_client import PostsClient
from pages.users_client import UsersClient


@pytest.fixture(scope="session")
def posts_client():
    """
    Fixture que devuelve un PostsClient compartido para todos los tests.

    scope="session" => se crea una vez por ejecución de pytest
    y se reutiliza en todos los tests que lo necesiten.
    """
    return PostsClient()


@pytest.fixture(scope="session")
def users_client():
    """
    Fixture que devuelve un UsersClient compartido para todos los tests.
    """
    return UsersClient()