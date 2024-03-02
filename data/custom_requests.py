import requests
import allure


class BaseRequests:
    host = 'https://stellarburgers.nomoreparties.site'

    def exec_post_request_with_token(self, url, data, token):
        headers = {'authorization': token}
        response = requests.post(url=url, data=data, headers=headers)
        if 'application/json' in response.headers['Content-Type']:
            return {"status_code": response.status_code, "text": response.json()}
        else:
            return {"status_code": response.status_code, "text": response.text}

    def exec_post_request(self, url, data):
        response = requests.post(url=url, data=data)
        if 'application/json' in response.headers['Content-Type']:
            return {"status_code": response.status_code, "text": response.json()}
        else:
            return {"status_code": response.status_code, "text": response.text}

    def exec_delete_request(self, url, token):
        headers = {"Content-Type": "application/json", 'authorization': token}
        response = requests.delete(url=url, headers=headers)
        return {"status_code": response.status_code, "text": response.json()}

    def exec_patch_request(self, url, data, token):
        headers = {'authorization': token}
        response = requests.patch(url=url, data=data, headers=headers)
        return {"status_code": response.status_code, "text": response.json()}

    def exec_get_request(self, url):
        response = requests.get(url=url, data={})
        return {"status_code": response.status_code, "text": response.json()}

    def exec_get_request_with_token(self, url, token):
        headers = {'authorization': token}
        response = requests.get(url=url, data={}, headers=headers)
        return {"status_code": response.status_code, "text": response.json()}


class UserRequests(BaseRequests):
    user_handler = '/api/auth/register'
    manipulate_user_handler = '/api/auth/user'
    user_login_handler = '/api/auth/login'

    @allure.step('Создаем пользователя, отправив запрос POST')
    def post_create_user(self, data=None):
        url = f"{self.host}{self.user_handler}"
        return self.exec_post_request(url=url, data=data)

    @allure.step('Логиним пользователя, отправив запрос POST')
    def post_login_user(self, token, data=None):
        url = f"{self.host}{self.user_login_handler}"
        return self.exec_post_request_with_token(url, data=data, token=token)

    @allure.step('Удаляем пользователя, отправив запрос DELETE')
    def delete_user(self, token):
        url = f"{self.host}{self.manipulate_user_handler}"
        return self.exec_delete_request(url, token=token)

    @allure.step('Обновляем данные пользователя, отправив запрос PATCH')
    def patch_user(self, data, token):
        url = f"{self.host}{self.manipulate_user_handler}"
        return self.exec_patch_request(url, data=data, token=token)

    @allure.step('Получаем данные пользователя, отправив запрос GET')
    def get_user_data(self, token):
        url = f"{self.host}{self.manipulate_user_handler}"
        return self.exec_get_request_with_token(url, token=token)


class OrderRequests(BaseRequests):
    ingredients_handler = '/api/ingredients'
    order_handler = '/api/orders'

    @allure.step('Создаем заказ, отправив запрос POST')
    def post_create_order(self, token, data):
        url = f"{self.host}{self.order_handler}"
        return self.exec_post_request_with_token(url, data=data, token=token)

    @allure.step('Создаем заказ без токена, отправив запрос POST')
    def post_create_order_no_token(self, data):
        url = f"{self.host}{self.order_handler}"
        return self.exec_post_request(url, data=data)

    @allure.step('Получаем список ингредиентов, отправив запрос GET')
    def get_ingredients_list(self):
        url = f"{self.host}{self.ingredients_handler}"
        return self.exec_get_request(url)

    @allure.step('Получаем заказы пользователя, отправив запрос GET.')
    def get_user_orders(self, token):
        url = f"{self.host}{self.order_handler}"
        return self.exec_get_request_with_token(url, token=token)
