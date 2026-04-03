from typing import Any

from pydantic import BaseModel


class GenericResponse[T: BaseModel | None](BaseModel):
    data: T | None
    code: str | None
    message: str | None


class EmptyResponse(BaseModel):
    pass


class CheckBalanceCredBlockModel(BaseModel):
    cred_block: dict[str, Any]
    customer_vpa: str
    bank_account_unique_id: str
    upi_request_id: str


class CheckBalanceResponseModel(BaseModel):
    balance: str | None
    outstanding_balance: str | None
    bank_account_unique_id: str


class AtomicBankModel(BaseModel):
    code: str | None
    mobRegFormat: str | None
    name: str | None
    referenceId: str | None
    upiEnabled: str | None
    isPopular: str | None


class ListBanksResponseModel(BaseModel):
    banks: list[AtomicBankModel]


class BankConsentRequestModel(BaseModel):
    consent_type: str = "aadhaar"
    bank_account_unique_id: str


class SetMpinRequestModel(BaseModel):
    type: str
    customer_vpa: str
    bank_account_unique_id: str
    card_last_six_digits: str | None
    expiry_month: str | None
    expiry_year: str | None
    cred_block: dict[str, Any]
    upi_request_id: str


class ChangeMpinCredBlockModel(BaseModel):
    cred_block: dict[str, Any]
    customer_vpa: str
    bank_account_unique_id: str
    upi_request_id: str


class VerifyVpaRequestModel(BaseModel):
    upi_number: str | None
    bank_account_number: str | None
    ifsc: str | None
    upi_string: str | None
    bharat_qr: str | None


class TpapAuthSession(BaseModel):
    customer_id: str
    device_id: str
    phone_number: str
    country_code: str
    npci_token: str
    npci_token_decoded: str
    device_fingerprint: str
    sim_slot: str
    status: str
    sms_token: str
    token_expiry_time: str | None
    system_time: str | None
