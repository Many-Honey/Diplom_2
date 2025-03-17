import allure
import requests
from data import Data
from urls import URL_ORDER


class TestGetUsersOrder:

    @allure.title('Получение заказов конкретного пользователя с авторизацией')
    def test_get_order_of_authorized_user_success(self, login_user):
        headers = login_user
        response_get_order = requests.get(URL_ORDER, headers=headers)
        assert response_get_order.status_code == 200
        assert response_get_order.json()["success"] == True
        assert response_get_order.json()["orders"] == []

    @allure.title('Получение заказов конкретного пользователя без авторизации')
    def test_get_order_of_not_authorized_user(self):
        response_get_order = requests.get(URL_ORDER)
        assert response_get_order.status_code == 401
        assert response_get_order.json()["success"] == False
        assert response_get_order.json()["message"] == Data.not_authorized