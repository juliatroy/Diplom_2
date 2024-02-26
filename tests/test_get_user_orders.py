import allure
from data.custom_requests import OrderRequests, UserRequests


@allure.feature('Проверка создания заказов')
class TestGetOrderForUser:
    @allure.title('Получить список заказов авторизованного пользователя')
    def test_get_user_orders_for_authorized_user(self, make_user, create_order_payload, create_user_payload):
        user_payload = create_user_payload(email='rand', password='rand', name='rand')
        user = make_user(data=user_payload)
        logged_user = UserRequests().post_login_user(data=user_payload, token=user['accessToken'])
        order_payload = create_order_payload
        token = logged_user['accessToken']
        order = OrderRequests().post_create_order(data=order_payload, token=token)
        resp = OrderRequests().get_user_orders(token=token)
        assert order["order"]["number"] == resp["orders"][0]["number"]

    @allure.title('Получить список заказов неавторизованного пользователя')
    def test_get_user_orders_for_unauthorized_user(self, make_user, create_order_payload, create_user_payload):
        user_payload = create_user_payload(email='rand', password='rand', name='rand')
        user = make_user(data=user_payload)
        order_payload = create_order_payload
        token = user['accessToken']
        order = OrderRequests().post_create_order(data=order_payload, token=token)
        resp = OrderRequests().get_user_orders(token=token)
        assert order["order"]["number"] == resp["orders"][0]["number"]

    @allure.title('Получить список заказов без токена')
    def test_get_user_orders_for_invalid_token(self, make_user, create_order_payload, create_user_payload):
        user_payload = create_user_payload(email='rand', password='rand', name='rand')
        user = make_user(data=user_payload)
        order_payload = create_order_payload
        token = user['accessToken']
        OrderRequests().post_create_order(data=order_payload, token=token)
        resp = OrderRequests().get_user_orders(status=401, token=None)
        assert resp["message"] == "You should be authorised"
