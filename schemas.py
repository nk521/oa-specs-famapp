from enum import Enum
from typing import Any

from pydantic import BaseModel


class CredType(Enum):
    BAL_ENQ = "reqBalEnq"
    PAY = "pay"
    COLLECT = "collect"
    SET_MPIN = "setMpin"
    CHANGE_MPIN = "changeMpin"
    BAL_CHECK = "reqBalChk"
    MANDATE = "mandate"
    UPI_LITE_ONBOARDING = "binding"
    UPI_LITE_PAY = "pay"


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


class RemoveBankAccountRequestModel(BaseModel):
    bank_account_unique_id: str


class UserAccountModel(BaseModel):
    vpas: list[VpaAddressModel]
    accounts: list[AtomicBankModel]
    default_vpa_address: str


class UserAccountsModel(
    BaseModel
):  # yes this and UserAccountModel are two different models
    vpas: list[VpaAddressModel]
    accounts: list[BankAccountAtomicModel]
    default_vpa_address: str


class VpaAddressModel(BaseModel):
    address: str
    is_merchant: str | None
    name: str | None
    ifsc: str | None
    type: str | None
    category: str | None
    bank_account_unique_id: str | None


class VerifyVpaRequestModel(BaseModel):
    upi_number: str | None
    bank_account_number: str | None
    ifsc: str | None
    upi_string: str | None
    bharat_qr: str | None


class ChangeDefaultAccountRequestModel(BaseModel):
    bank_account_unique_id: str


class GenerateOtpRequestModel(BaseModel):
    type: str | None
    customer_vpa: str | None
    bank_account_unique_id: str | None
    card_last_six_digits: str | None
    expiry_month: str | None
    expiry_year: str | None
    aadhaar_first_six_digits: str | None
    cred_block_dto: CredBlockRequestModel | None


class CredBlockRequestModel(BaseModel):
    amount: str
    cred_type: list[str]
    payee_vpa: str
    payer_vpa: str
    bank_account_unique_id: str
    note: str | None
    ref_id: str | None
    ref_url: str | None  # assumed based on ref_id, this key is encrypted in source
    channel: str | None

    @classmethod
    def generate_for_set_mpin(cls, bank_account_unique_id: str, customer_vpa: str):
        cls.amount = "0"
        cls.cred_type = [CredType.SET_MPIN.value]
        cls.payee_vpa = customer_vpa
        cls.payer_vpa = customer_vpa
        cls.bank_account_unique_id = bank_account_unique_id
        # Channel is 480 in this context. It goes thru this block --
        # (i & 256) != 0 ? null : "LITE"
        cls.channel = None


class UpiRequestTypeIdModel(BaseModel):
    cred_type: str
    upi_request_id: str


class credBlockAtomicResponse(BaseModel):
    key_code: str
    xml_payload: str
    controls: str
    configuration: str
    salt: str
    trust: str
    pay_info: str
    language_pref: str
    upi_request_id: list[UpiRequestTypeIdModel]  # note: not a type, key is singular
    trust_non_sha: str


class CredBlockResponse(BaseModel):
    cred_block: credBlockAtomicResponse | None


class BankAccountAtomicModel(BaseModel):
    bank_account_unique_id: str
    bank_code: str
    bank_name: str
    name: str
    mask_account_number: str
    mpin_set: bool
    mpin_length: str
    type: str
    ifsc: str
    atm_pin_length: str
    is_default: bool


class LinkedBankAccountsResponseModel(BaseModel):
    accounts: list[BankAccountAtomicModel]


class AddBankAccountRequestModel(BaseModel):
    bank_account_unique_id: str
    not_default: str


class UpiLiteOnboardingRequestModel(BaseModel):
    cred_block: dict[str, Any]
    bank_account_unique_id: str
    upi_request_id: str


class UpiLiteOnboardingResponseModel(BaseModel):
    resp_list_keys: str | None
    resp_list_keys_expiry: int | None
    lite_bank_account: UpiLiteAccountDetails | None


class UpiLiteAccountDetails(BaseModel):
    name: str | None
    account_number: str | None  # AKA liteReferenceNumber
    bank_account_unique_id: str | None
    first_top_up_done: bool | None


class UpiLiteSyncResponseModel(BaseModel):
    lrn: str | None  # liteReferenceNumber
    arpc: str | None


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
