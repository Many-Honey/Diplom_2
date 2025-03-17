import allure
import requests
from data import Data
from urls import URL_ORDER


class TestMakeOrder:
    @allure.title('Создание заказа авторизованным пользователем')
    def test_make_order_authorized_user_success(self, login_user, order_request_body):
        headers = login_user
        payload_order = order_request_body
        response_order = requests.post(URL_ORDER, data=payload_order, headers=headers)
        assert response_order.status_code == 200
        assert "number" in  response_order.json()["order"]
        assert response_order.json()["success"] == True

    @allure.title('Создание заказа без ингредиентов')
    def test_make_order_without_ingredients_authorized_user(self, login_user):
        headers = login_user
        payload_order = {
            "ingredients": []
        }
        response_order = requests.post(URL_ORDER, data=payload_order, headers=headers)
        assert response_order.status_code == 400
        assert response_order.json()["success"] == False
        assert response_order.json()["message"] == Data.no_ingredients

    @allure.title('Создание заказа с неверным хешем ингредиентов')
    def test_make_order_with_invalid_ingredients_authorized_user(self, login_user):
        headers = login_user
        response_order = requests.post(URL_ORDER, data=Data.payload_order, headers=headers)
        assert response_order.status_code == 500

    @allure.title('Создание заказа неавторизованным пользователем')
    def test_make_order_not_authorized_user_fail(self, order_request_body):
        payload_order = order_request_body
        response_order = requests.post(URL_ORDER, data=payload_order)
        assert response_order.status_code == 401
        assert response_order.json()["success"] == False
        assert response_order.json()["message"] == Data.not_authorized