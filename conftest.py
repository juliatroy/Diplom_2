import random

import pytest
from faker import Faker
import allure
from data.custom_requests import UserRequests
from data.custom_requests import OrderRequests

fake = Faker()


@pytest.fixture
def create_user_payload():
    @allure.step('Конструируем payload для пользователя')
    def _create_user_payload(name=None, email=None, password=None):
        payload = {}
        if name == 'rand':
            payload["name"] = fake.name()
        elif name is not None:
            payload["name"] = name
        if password == 'rand':
            payload["password"] = fake.pyint()
        elif password is not None:
            payload["password"] = password
        if email == 'rand':
            payload["email"] = fake.email()
        elif email is not None:
            payload["email"] = email
        return payload

    return _create_user_payload


@pytest.fixture
@allure.step('Создаем случайное число')
def make_random_value():
    return fake.pyint()

@pytest.fixture
@allure.step('Создаем случайное имя пользователя')
def make_fake_name():
    return fake.name()


@pytest.fixture
@allure.step('Конструируем payload для отправки заказа')
def create_order_payload():
    ingredients_list = OrderRequests().get_ingredients_list()
    ids = [element['_id'] for element in ingredients_list['data']]
    ids_for_payload = random.sample(ids, 3)
    payload = {"ingredients": ids_for_payload}
    return payload


@pytest.fixture(scope='function')
def make_user():
    user = {}

    def _make_user(data):
        nonlocal user
        user_requests = UserRequests()
        user = user_requests.post_create_user(data=data)
        return user

    yield _make_user
    UserRequests().delete_user(token=user['accessToken'])


@pytest.fixture(scope='function')
def del_user():
    user = {}
    yield user
    UserRequests().delete_user(token=user['token'])


