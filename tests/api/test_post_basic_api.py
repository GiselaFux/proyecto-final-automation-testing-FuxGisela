import pytest
from pytest_check import check


@pytest.mark.api
class TestPostsBasicAPI:
    # Tests básicos sobre /posts:
   

    def test_get_all_posts_returns_200_and_list(self, posts_client):
        # Arrange / Act
        response = posts_client.get_all_posts()

        # Assert
        # assert response.status_code == 200
        check.equal(response.status_code, 200, "La API no respondió con el código esperado")
        data = response.json()
        #assert isinstance(data, list)
        check.is_true(isinstance(data, list), "La respuesta no es una lista")
        #assert len(data) > 0
        check.is_true(len(data) > 0, "La lista de posts está vacía")
        #assert "id" in data[0]
        check.is_true("id" in data[0], "El primer post no tiene el campo 'id'")
        #assert "title" in data[0]
        check.is_true("title" in data[0], "El primer post no tiene el campo 'title'")

    def test_get_post_by_id_returns_correct_post(self, posts_client):
        post_id = 1

        response = posts_client.get_post_by_id(post_id)

        #assert response.status_code == 200
        check.equal(response.status_code, 200, f"La API no respondió con el código esperado para el post ID {post_id}")
        data = response.json()
        #assert data["id"] == post_id
        check.equal(data["id"], post_id, f"El ID del post no coincide con el ID solicitado: {post_id}")
        #assert "title" in data
        check.is_true("title" in data, "El post no tiene el campo 'title'")

    def test_create_post_returns_201_or_200(self, posts_client):
        payload = {
            "title": "mi post de prueba",
            "body": "contenido de ejemplo",
            "userId": 1,
        }

        response = posts_client.create_post(payload)

        #assert response.status_code in (201, 200)
        check.is_true(response.status_code in (201, 200), "La API no respondió con el código esperado al crear un post")
        data = response.json()
        #assert data.get("title") == payload["title"]
        check.equal(data.get("title"), payload["title"], "El título del post creado no coincide con el título enviado en el payload")
        #assert data.get("body") == payload["body"]
        check.equal(data.get("body"), payload["body"], "El cuerpo del post creado no coincide con el cuerpo enviado en el payload")
        #assert "id" in data
        check.is_true("id" in data, "El post creado no tiene el campo 'id'")

    def test_create_post_with_all_fields_returns_201_or_200(self, posts_client):
        payload = {
            "title": "mi post de prueba 2",
            "body": "contenido de ejemplo 2",
            "userId": 1
        }
        response = posts_client.create_post(payload)
        assert response.status_code in (201, 200)
        
    def test_delete_post_returns_200(self, posts_client):
        post_id = 1
        response = posts_client.delete_post(post_id)
        # assert response.status_code == 200 
        check.equal(response.status_code, 200, "El post no fue eliminado correctamente por ser api de prueba.Puede retornar 200 pero el post no existe")   
        
    def test_verify_deleted_post(self, posts_client):
        post_id = 1
        response = posts_client.get_post_by_id(post_id)
        #  assert response.status_code == 404  or response.status_code == 200
        check.equal(response.status_code, 404, "El post no fue eliminado correctamente por ser api de prueba.Puede retornar 200 pero el post no existe")
        
