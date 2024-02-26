import requests
import allure


class BaseRequests:
    host = 'https://stellarburgers.nomoreparties.site'

    def exec_post_request_and_check(self, url, data, status, token=None):
        headers = {}
        if token is not None:
            headers.update({'authorization': token})
        response = requests.post(url=url, data=data, headers=headers)
        assert response.status_code == status
        if 'application/json' in response.headers['Content-Type']:
            return response.json()
        else:
            return response.text

    def exec_delete_request_and_check(self, url, status, token):
        headers = {"Content-Type": "application/json", 'authorization': token}
        response = requests.delete(url=url, headers=headers)
        assert response.status_code == status
        if 'application/json' in response.headers['Content-Type']:
            return response.json()
        else:
            return response.text

    def exec_patch_request_and_check(self, url, data, token, status):
        headers = {'authorization': token}
        response = requests.patch(url=url, data=data, headers=headers)
        assert response.status_code == status
        if 'application/json' in response.headers['Content-Type']:
            return response.json()
        else:
            return response.text

    def exec_get_request_and_check(self, url, status, token=None):
        headers = None
        if token is not None:
            headers = {'authorization': token}
        data = {}
        response = requests.get(url=url, data=data, headers=headers)
        assert response.status_code == status
        if 'application/json' in response.headers['Content-Type']:
            return response.json()
        else:
            return response.text


class UserRequests(BaseRequests):
    user_handler = '/api/auth/register'
    manipulate_user_handler = '/api/auth/user'
    user_login_handler = '/api/auth/login'

    @allure.step('Создаем пользователя, отправив запрос POST. Ожидаем статус респонса {status}')
    def post_create_user(self, data=None, status=200):
        url = f"{self.host}{self.user_handler}"
        return self.exec_post_request_and_check(url, data=data, status=status)

    @allure.step('Логиним пользователя, отправив запрос POST. Ожидаем статус респонса {status}')
    def post_login_user(self, token, data=None, status=200):
        url = f"{self.host}{self.user_login_handler}"
        return self.exec_post_request_and_check(url, data=data, status=status, token=token)

    @allure.step('Удаляем пользователя, отправив запрос DELETE. Ожидаем статус респонса {status}')
    def delete_user(self, token=None, status=202):
        url = f"{self.host}{self.manipulate_user_handler}"
        return self.exec_delete_request_and_check(url, status=status, token=token)

    @allure.step('Обновляем данные пользователя, отправив запрос PATCH. Ожидаем статус респонса {status}')
    def patch_user(self, data=None, token=None, status=200):
        url = f"{self.host}{self.manipulate_user_handler}"
        return self.exec_patch_request_and_check(url, data=data, status=status, token=token)

    @allure.step('Получаем данные пользователя, отправив запрос GET. Ожидаем статус респонса {status}')
    def get_user_data(self, token, status=200):
        url = f"{self.host}{self.manipulate_user_handler}"
        return self.exec_get_request_and_check(url, status=status, token=token)


class OrderRequests(BaseRequests):
    ingredients_handler = '/api/ingredients'
    order_handler = '/api/orders'

    @allure.step('Создаем заказ, отправив запрос POST. Ожидаем статус респонса {status}')
    def post_create_order(self, token, data=None, status=200):
        url = f"{self.host}{self.order_handler}"
        return self.exec_post_request_and_check(url, data=data, status=status, token=token)

    @allure.step('Получаем список ингредиентов, отправив запрос GET. Ожидаем статус респонса {status}')
    def get_ingredients_list(self, status=200):
        url = f"{self.host}{self.ingredients_handler}"
        return self.exec_get_request_and_check(url, status=status)

    @allure.step('Получаем заказы пользователя, отправив запрос GET. Ожидаем статус респонса {status}')
    def get_user_orders(self, token, status=200):
        url = f"{self.host}{self.order_handler}"
        return self.exec_get_request_and_check(url, status=status, token=token)


