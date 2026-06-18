import pytest


@pytest.mark.api
class TestUsersAPI:
    """
    Tests sobre /users:
    - GET lista de usuarios y validación de campos mínimos.
    """

    def test_get_users_returns_list_with_required_fields(self, users_client):
        response = users_client.get_all_users()

        assert response.status_code == 200
        users = response.json()
        assert isinstance(users, list)
        assert len(users) > 0

        for user in users:
            assert "id" in user
            assert "name" in user
            assert "email" in user
            
            
    def test_get_user_by_id_returns_correct_user(self, users_client):   
       user_id = 1
       response = users_client.get_user_by_id(user_id)  
       assert response.status_code == 200
       users = response.json()
       assert users["id"] == user_id
       assert "name" in users
       assert "email" in users
       
       
    def test_get_users_tipo_campos(self,users_client):
        response = users_client.get_all_users()
        assert response.status_code == 200
        users = response.json()
        for user in users:
            assert isinstance(user["id"], int)
            assert isinstance(user["name"], str)
            assert isinstance(user["email"], str)
           
           
    def test_get_users_email_format(self,users_client):
       response = users_client.get_all_users()
       assert response.status_code == 200
       users = response.json()
       for user in users:
           assert "@" in user["email"]
           
    def test_get_users_name_mayor_2_caracteres(self,users_client):
       response = users_client.get_all_users() 
       assert response.status_code == 200   
       users =response.json()
       for user in users:
            assert len(user["name"]) > 2 