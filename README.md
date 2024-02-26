Diploma part 2 of 'QA Automation Python' course of Yandex.Praktikum.

Topic: API tests

Author: Julia Troy

Libraries used:
- pytest
- allure-pytest
- requests
- faker
- random

Tests implemented:
    TestCreateUser
        test_can_create_user
        test_cant_create_user_dupes
        test_all_the_fields_are_required
    TestUserLogin
        test_existing_user_can_log_in
        test_user_with_wrong_info_cant_login
    TestUserDataUpdate
        test_can_patch_unauthorized_user
        test_can_patch_authorized_user
        test_cant_patch_user_with_wrong_token
    TestOrderOptions
        test_create_order_for_unauthorized_user
        test_create_order_for_authorized_user
        test_create_order_no_ingredients
        test_create_order_wrong_ingredients_id
        test_create_order_token_no_ingredients
        test_create_order_token_wrong_ingredients_id
    TestGetOrderForUser
        test_get_user_orders_for_authorized_user
        test_get_user_orders_for_unauthorized_user
        test_get_user_orders_for_invalid_token