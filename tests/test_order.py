import allure

from data.custom_requests import OrderRequests


@allure.feature('Проверка создания заказов')
class TestOrderOptions:
    @allure.title('Можно создать заказ без токена пользователя и ингредиентами')
    def test_create_order_for_unauthorized_user(self, create_order_payload):
        payload = create_order_payload
        assert OrderRequests().post_create_order(data=payload, token=None)

    @allure.title('Можно создать заказ с токеном пользователя и ингредиентами')
    def test_create_order_for_authorized_user(self, create_order_payload, make_user, create_user_payload):
        user_payload = create_user_payload(email='rand', password='rand', name='rand')
        user = make_user(data=user_payload)
        order_payload = create_order_payload
        token = user['accessToken']
        resp = OrderRequests().post_create_order(data=order_payload, token=token)
        assert resp["success"]

    @allure.title('Нельзя создать заказ без ингредиентов')
    def test_create_order_no_ingredients(self):
        payload = {}
        response = OrderRequests().post_create_order(data=payload, status=400, token=None)
        assert response["message"] == 'Ingredient ids must be provided'

    @allure.title('Нельзя создать заказ с неверным id ингредиента')
    def test_create_order_wrong_ingredients_id(self, create_order_payload, make_random_value):
        payload = create_order_payload
        payload["ingredients"][0] = payload["ingredients"][0]+str(make_random_value)
        resp = OrderRequests().post_create_order(data=payload, status=500, token=None)
        assert 'Internal Server Error' in resp

    @allure.title('Нельзя создать заказ с токеном и без ингредиентов')
    def test_create_order_token_no_ingredients(self, make_user, create_user_payload):
        user_payload = create_user_payload(email='rand', password='rand', name='rand')
        user = make_user(data=user_payload)
        token = user['accessToken']
        payload = {}
        response = OrderRequests().post_create_order(data=payload, status=400, token=token)
        assert response["message"] == 'Ingredient ids must be provided'

    @allure.title('Нельзя создать заказ с токеном и неверным id ингредиента')
    def test_create_order_token_wrong_ingredients_id(self, create_order_payload, make_random_value, create_user_payload,
                                                     make_user):
        user_payload = create_user_payload(email='rand', password='rand', name='rand')
        user = make_user(data=user_payload)
        token = user['accessToken']
        payload = create_order_payload
        payload["ingredients"][0] = payload["ingredients"][0]+str(make_random_value)
        resp = OrderRequests().post_create_order(data=payload, status=500, token=token)
        assert 'Internal Server Error' in resp
