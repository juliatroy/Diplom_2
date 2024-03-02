import pytest
from data.custom_requests import UserRequests
import allure


@allure.feature('Проверка обновления данных юзера')
class TestUserDataUpdate:
    @pytest.mark.parametrize("key_to_be_changed",
                             ["email",
                              "password",
                              "name"]
                             )
    @allure.title('Изменение данных пользователя без авторизации')
    def test_can_patch_unauthorized_user(self, create_user_payload, make_user, key_to_be_changed, make_random_value):
        payload = create_user_payload(email='rand', password='1234', name='rand')
        user = make_user(data=payload)
        payload[key_to_be_changed] = make_random_value
        patched_user = UserRequests().patch_user(data=payload, token=user["text"]['accessToken'])
        updated_user = UserRequests().get_user_data(token=user["text"]['accessToken'])
        assert (patched_user["text"]["user"]["name"] == updated_user["text"]["user"]["name"] and
                patched_user["text"]["user"]["email"] == updated_user["text"]["user"]["email"])

    @pytest.mark.parametrize("key_to_be_changed",
                             ["email",
                              "password",
                              "name"]
                             )
    @allure.title('Изменение данных пользователя с авторизацей')
    def test_can_patch_authorized_user(self, create_user_payload, make_user, key_to_be_changed, make_fake_name):
        payload = create_user_payload(email='rand', password='1234', name='rand')
        user = make_user(data=payload)
        UserRequests().post_login_user(data=payload, token=user["text"]['accessToken'])
        payload[key_to_be_changed] = make_fake_name
        UserRequests().patch_user(data=payload, token=user["text"]['accessToken'])
        updated_user = UserRequests().get_user_data(token=user["text"]['accessToken'])
        assert (payload["name"] == updated_user["text"]["user"]["name"] and
                payload["email"].lower() == updated_user["text"]["user"]["email"])


    @pytest.mark.parametrize("key_to_be_changed",
                             ["email",
                              "password",
                              "name"]
                             )
    @allure.title('Изменение данных пользователя с невалидным токеном')
    def test_cant_patch_user_with_wrong_token(self, create_user_payload, make_user, key_to_be_changed, make_random_value):
        payload = create_user_payload(email='rand', password='1234', name='rand')
        user = make_user(data=payload)
        new_payload = payload
        new_payload[key_to_be_changed] = make_random_value
        token = user["text"]['accessToken'] + str(make_random_value)
        resp = UserRequests().patch_user(data=new_payload, token=token)
        updated_user = UserRequests().get_user_data(token=user["text"]['accessToken'])
        assert (resp["status_code"] == 403 and updated_user["text"]["user"]["name"] == user["text"]["user"]["name"]
                and updated_user["text"]["user"]["email"] == user["text"]["user"]["email"])

