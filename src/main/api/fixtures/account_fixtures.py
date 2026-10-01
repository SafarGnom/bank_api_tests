import pytest


@pytest.fixture
def create_user_account(api_manager, create_user_request):
    return api_manager.user_steps.create_account(create_user_request)


@pytest.fixture
def create_credit_account(api_manager, create_user_credit_request):
    return api_manager.user_steps.create_account(
        create_user_credit_request)


@pytest.fixture
def create_two_accounts(api_manager, create_user_request):
    account_1 = api_manager.user_steps.create_account(create_user_request)

    account_2 = api_manager.user_steps.create_account(create_user_request)

    return account_1, account_2


@pytest.fixture
def create_two_credit_accounts(api_manager, create_user_credit_request):
    account_1 = api_manager.user_steps.create_account(create_user_credit_request)

    account_2 = api_manager.user_steps.create_account(create_user_credit_request)

    return account_1, account_2
