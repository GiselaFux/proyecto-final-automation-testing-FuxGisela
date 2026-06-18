# pages/posts_client.py
from typing import Dict, Any

from .base_client import BaseAPIClient


class PostsClient(BaseAPIClient):
    """
    Client para el recurso /posts de JSONPlaceholder.

    Proporciona métodos de alto nivel para:
    - obtener todos los posts
    - obtener un post por id
    - crear un post
    - actualizar un post (PUT/PATCH)
    - eliminar un post
    """

    def get_all_posts(self):
        return self.get("/posts")

    def get_post_by_id(self, post_id: int):
        return self.get(f"/posts/{post_id}")

    def create_post(self, payload: Dict[str, Any]):
        return self.post("/posts", json=payload)

    def update_post_put(self, post_id: int, payload: Dict[str, Any]):
        return self.put(f"/posts/{post_id}", json=payload)

    def update_post_patch(self, post_id: int, payload: Dict[str, Any]):
        return self.patch(f"/posts/{post_id}", json=payload)

    def delete_post(self, post_id: int):
        return self.delete(f"/posts/{post_id}")