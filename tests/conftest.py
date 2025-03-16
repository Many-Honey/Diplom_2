import string
import random
import pytest
import requests
from urls import *


# фикстура возвращает тело запроса для создания нового пользователя и удаляет созданного пользователя в конце теста
@pytest.fixture
def user_request_body(request_body):
    payload = request_body
    yield payload
    # формируем тело запроса для входа в систему
    payload_login = {
        "email": payload.get("email"),
        "password": payload.get("password")
    }
    # отправляем запрос на вход в систему
    response_login = requests.post(URL_USER_LOGIN, data=payload_login)
    # получаем значение accessToken
    r = response_login.json()
    access_token = r.get("accessToken")
    headers = {"Authorization": f"Bearer{access_token}"}
    # удаляем созданного ранее пользователя
    response_delete = requests.delete(URL_USER, headers=headers)
    print(response_delete.text)

# фикстура регистрирует нового пользователя и удаляет созданного пользователя в конце теста
@pytest.fixture
def user_registration(request_body):
    payload = request_body
    response_reg = requests.post(URL_USER_REGISTER, payload)
    yield payload
    # получаем значение accessToken
    r = response_reg.json()
    access_token = r.get("accessToken")
    headers = {"Authorization": f"Bearer{access_token}"}
    # удаляем созданного ранее пользователя
    response_delete = requests.delete(URL_USER, headers=headers)
    print(response_delete.text)

# фикстура возвращает тело запроса для создания нового пользователя
@pytest.fixture
def request_body():
    # метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    # генерируем имейл, пароль и имя пользователя
    email = generate_random_string(10)
    password = generate_random_string(10)
    name = generate_random_string(10)
    # собираем тело запроса
    payload = {
        "email": f'{email}@yandex.ru',
        "password": password,
        "name": name
    }
    # возвращаем тело запроса
    return payload

@pytest.fixture
def order_request_body():
    response = requests.get(URL_INGREDIENTS)
    def random_i(a):
        number = len(a) - 1
        n = random.randint(0, number)
        return n
    ingredients = []
    for i in range(0,2):
        ingredients.append(response.json()["data"][random_i(response.json()["data"])]["_id"])
    payload = {
        "ingredients": ingredients
    }
    return payload

@pytest.fixture
def login_user(request_body):
    payload = request_body
    requests.post(URL_USER_REGISTER, payload)
    payload_login = {
        "email": request_body.get("email"),
        "password": request_body.get("password")
    }
    response_login = requests.post(URL_USER_LOGIN, data=payload_login)
    r = response_login.json()
    access_token = r.get("accessToken")
    headers = {"Authorization": f"Bearer{access_token}"}
    yield headers
    response_delete = requests.delete(URL_USER, headers=headers)
    print(response_delete.text)
