import allure
import pytest
import requests
from urls import URL_USER_REGISTER


class TestUserRegister:

    # сообщение при попытке регистрации уже зарегистрированного пользователя
    message_1 = "User already exists"
    # сообщение при попытке регистрации без заполнения одного из обязательных полей
    message_2 = "Email, password and name are required fields"

    @allure.title('Создание уникального пользователя')
    def test_successful_user_registration(self, user_request_body):
        payload = user_request_body
        response = requests.post(URL_USER_REGISTER, payload)
        assert response.status_code == 200
        assert response.json()["success"] == True
        assert "accessToken" in response.json()
        assert "refreshToken" in response.json()
        assert response.json()["user"]["email"] == payload.get("email")
        assert response.json()["user"]["name"] == payload.get("name")

    @allure.title('Создание пользователя, который уже зарегистрирован')
    def test_create_already_registered_user(self, user_request_body):
        payload = user_request_body
        response_1 = requests.post(URL_USER_REGISTER, payload)
        assert response_1.status_code == 200
        response_2 = requests.post(URL_USER_REGISTER, payload)
        assert response_2.status_code == 403
        assert response_2.json()["success"] == False
        assert response_2.json()["message"] == self.message_1

    @allure.title('Создание пользователя без указания обязательных полей')
    @pytest.mark.parametrize("required_field", ["email", "password", "name"])
    def test_create_user_without_required_fields(self, user_request_body, required_field):
        payload = user_request_body
        payload[required_field] = ""
        response = requests.post(URL_USER_REGISTER, payload)
        assert response.status_code == 403
        assert response.json()["success"] == False
        assert response.json()["message"] == self.message_2




