import allure
import pytest
import requests
from tests.conftest import user_registration
from urls import URL_USER_LOGIN


class TestLogin:
    @allure.title('Логин под существующим пользователем')
    def test_successful_login(self, user_registration):
        payload = user_registration
        payload_login = {
            "email": payload.get("email"),
            "password": payload.get("password")
        }
        response_login = requests.post(URL_USER_LOGIN, data=payload_login)
        assert response_login.status_code == 200
        assert response_login.json()["success"] == True
        assert "accessToken" in response_login.json()
        assert "refreshToken" in response_login.json()
        assert response_login.json()["user"]["email"] == payload.get("email")
        assert response_login.json()["user"]["name"] == payload.get("name")

    @allure.title('Логин с неверным логином и паролем')
    @pytest.mark.parametrize("invalid_data, data_value", [["email", "wrong_mail@yandex.ru"], ["password", "wrong_password"]])
    def test_login_with_wrong_email_or_password(self, user_registration, invalid_data, data_value):
        payload = {"email": user_registration.get("email"), "password": user_registration.get("password")}
        payload_login = payload
        payload_login[invalid_data] = data_value
        response_login = requests.post(URL_USER_LOGIN, data=payload_login)
        assert response_login.status_code == 401
        assert response_login.json()["success"] == False
        assert response_login.json()["message"] == "email or password are incorrect"


