from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.create_credit_repay_request import CreateCreditRepayRequest
from src.main.api.models.create_credit_request import CreateCreditRequest
from src.main.api.models.create_credit_user_request import CreateCreditUserRequest
from src.main.api.models.create_deposit_request import CreateDepositRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.sepcs.request_specs import RequestSpecs
from src.main.api.sepcs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    def create_account(self,create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_created()
        ).post()
        return response

    def create_account_bad(self,create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_conflict()
        ).post()
        return response

    def get_credit(self, create_user_credit_request: CreateCreditUserRequest, create_credit_request: CreateCreditRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_credit_request.username,
                password=create_user_credit_request.password
            ),
            Endpoint.CREATE_CREDIT,
            ResponseSpecs.request_created()
        ).post(create_credit_request)

        return response

    def get_credit_bad(self, create_user_credit_request: CreateCreditUserRequest, create_credit_request: CreateCreditRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_credit_request.username,
                password=create_user_credit_request.password
            ),
            Endpoint.CREATE_CREDIT,
            ResponseSpecs.request_not_found()
        ).post(create_credit_request)

        return response

    def create_account_deposit(self,create_user_request: CreateUserRequest, create_deposit_request: CreateDepositRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREATE_ACCOUNT_DEPOSIT,
            ResponseSpecs.request_ok()
        ).post(create_deposit_request)
        return response


    def create_account_deposit_bad(self,create_user_request: CreateUserRequest, create_deposit_request: CreateDepositRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREATE_ACCOUNT_DEPOSIT,
            ResponseSpecs.request_bad()
        ).post(create_deposit_request)
        return response



    def transfer_between_accounts(self, create_user_request: CreateUserRequest,
                                   transfer_between_accounts: TransferRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.TRANSFER_BETWEEN_ACCOUNTS,
            ResponseSpecs.request_ok()
        ).post(transfer_between_accounts)
        return response

    def transfer_between_accounts_bad(self, create_user_request: CreateUserRequest,
                                   transfer_between_accounts: TransferRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.TRANSFER_BETWEEN_ACCOUNTS,
            ResponseSpecs.request_unprocessable_entity()
        ).post(transfer_between_accounts)
        return response

    def repay_credit(self,create_user_secret_role_request: CreateCreditUserRequest, repay_credit_request: CreateCreditRepayRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_secret_role_request.username,
                password=create_user_secret_role_request.password
            ),
            Endpoint.REPAY_CREDIT,
            ResponseSpecs.request_ok()
        ).post(repay_credit_request)

        return response


    def repay_credit_bad(self,create_user_secret_role_request: CreateCreditUserRequest, repay_credit_request: CreateCreditRepayRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_secret_role_request.username,
                password=create_user_secret_role_request.password
            ),
            Endpoint.REPAY_CREDIT,
            ResponseSpecs.request_unprocessable_entity()
        ).post(repay_credit_request)

        return response





















