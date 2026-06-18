import pytest


@pytest.mark.api
class TestPostsLifecycleAPI:
    """
    Demuestra un flujo completo usando /posts:

    - POST   -> crear
    - GET    -> verificar creación (hasta donde JSONPlaceholder lo permite)
    - PATCH  -> actualización parcial
    - GET    -> verificar actualización
    - DELETE -> borrar
    - GET    -> verificar borrado (comportamiento simulado)
    """

    def test_post_full_lifecycle_with_patch(self, posts_client):
        # 1. Crear un post
        create_payload = {
            "title": "post ciclo completo",
            "body": "contenido inicial",
            "userId": 1,
        }
        create_resp = posts_client.create_post(create_payload)

        assert create_resp.status_code in (201, 200)
        created = create_resp.json()
        created_id = created.get("id")
        assert created_id is not None

        # 2. GET del post recién creado (simulado)
        get_resp_1 = posts_client.get_post_by_id(created_id)
        # JSONPlaceholder es una API de prueba y a veces no refleja
        # exactamente la creación previa. Por eso aceptamos 200 o 404.
        assert get_resp_1.status_code in (200, 404)
        if get_resp_1.status_code == 200:
            data_1 = get_resp_1.json()
            assert data_1.get("id") == created_id

        # 3. PATCH: actualizar parcialmente el título
        patch_payload = {
            "title": "post ciclo completo (actualizado)",
        }
        patch_resp = posts_client.update_post_patch(created_id, patch_payload)
        assert patch_resp.status_code in (200, 204)
        patched = patch_resp.json()
        # En JSONPlaceholder normalmente devuelve el merge del payload
        assert patched.get("title") == patch_payload["title"]

        # 4. GET otra vez (validación limitada por la naturaleza de la API fake)
        get_resp_2 = posts_client.get_post_by_id(created_id)
        assert get_resp_2.status_code in (200, 404)
        if get_resp_2.status_code == 200:
            data_2 = get_resp_2.json()
            assert data_2.get("id") == created_id

        # 5. DELETE
        delete_resp = posts_client.delete_post(created_id)
        assert delete_resp.status_code in (200, 204)

        # 6. GET final (en una API real esperarías 404)
        get_resp_3 = posts_client.get_post_by_id(created_id)
        assert get_resp_3.status_code in (200, 404)