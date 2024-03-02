import pytest
import allure

from data.custom_requests import UserRequests


@allure.feature('Проверка создания юзера')
class TestCreateUser:
    @allure.title('Можно создать юзера со случайным логином')
    def test_can_create_user(self, create_user_payload, del_user):
        payload = create_user_payload(email='rand', password='1234', name='rand')
        user = UserRequests().post_create_user(data=payload)
        del_user.update({'token': user["text"]['accessToken']})
        assert user["status_code"] == 200 and user["text"]["success"]

    @allure.title('Нельзя создать двух юзеров с одинаковыми логинами')
    def test_cant_create_user_dupes(self, create_user_payload, make_user):
        payload = create_user_payload(email='rand', password='1234', name='rand')
        make_user(data=payload)
        resp_dupe = UserRequests().post_create_user(data=payload)
        assert resp_dupe["status_code"] == 403 and resp_dupe["text"]["message"] == "User already exists"

    @pytest.mark.parametrize("payload_schema",
                             [
                                 [None, 'rand', 'rand'],
                                 ['rand', None, 'rand'],
                                 ['rand', 'rand', None]
                             ])
    @allure.title('Для создания юзера необходимо задать все обязательные поля (email, пароль, имя)')
    def test_all_the_fields_are_required(self, payload_schema, create_user_payload):
        payload = create_user_payload(email=payload_schema[0], password=payload_schema[1],
                                      name=payload_schema[2])
        resp = UserRequests().post_create_user(data=payload)
        assert resp["status_code"] == 403 and resp["text"]["message"] == "Email, password and name are required fields"
