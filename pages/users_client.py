# pages/users_client.py
from .base_client import BaseAPIClient


class UsersClient(BaseAPIClient):
    """
    Client para el recurso /users de JSONPlaceholder.
    """

    def get_all_users(self):
        return self.get("/users")

    def get_user_by_id(self, user_id: int):
        return self.get(f"/users/{user_id}")