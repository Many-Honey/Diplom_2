import allure
import pytest
import requests
from urls import URL_USER_LOGIN, URL_USER


class TestChangeUserData:
    @allure.title('Изменение данных авторизованного пользователя')
    @pytest.mark.parametrize('change_data', ["name", "email", "password"])
    def test_change_user_data_authorized_user_success(self, user_registration, change_data):
        payload_login = {
            "email": user_registration.get("email"),
            "password": user_registration.get("password")
        }
        response_login = requests.post(URL_USER_LOGIN, data=payload_login)
        r = response_login.json()
        access_token = r.get("accessToken")
        headers = {"Authorization": f"Bearer{access_token}"}
        payload_change = {
            change_data: f'new_{user_registration[change_data]}'
        }
        response_change = requests.patch(URL_USER, data=payload_change, headers=headers)
        assert response_change.status_code == 200
        assert response_change.json()["success"] == True
        if change_data == "name" or change_data == "email":
            assert response_change.json()["user"][change_data] == payload_change[change_data]

    @allure.title('Изменение данных неавторизованного пользователя')
    @pytest.mark.parametrize('change_data', ["name", "email", "password"])
    def test_change_user_data_not_authorized_user(self, user_registration, change_data):
        payload_change = {
            change_data: f'new_{user_registration[change_data]}'
        }
        response_change = requests.patch(URL_USER, data=payload_change)
        assert response_change.status_code == 401
        assert response_change.json()["success"] == False
        assert response_change.json()["message"] == "You should be authorised"

