from fastapi import APIRouter, FastAPI

import schemas

base_url = "https://hogwarts.famapp.in/halfblood/"

app = FastAPI(
    title="Fampay Banking API",
    description="Internal API for managing UPI transactions, bank accounts, and VPA mappings.",
    version="1.0.0",
    servers=[{"url": base_url, "description": "Fampay's Prod Server"}],
)

# --- BANK ROUTES ---
r_BankRoutes = APIRouter(prefix="/bank", tags=["Bank Management"])


@r_BankRoutes.get(
    "/list",
    summary="List Supported Banks",
    description="Fetch a list of all NPCI-supported banks available for linking.",
)
def BankRoutes_list(
    showCreditLines: bool,
) -> schemas.GenericResponse[schemas.ListBanksResponseModel]: ...


@r_BankRoutes.post(
    "/account/consent",
    summary="Account Linking Consent",
    description="Retrieve or submit user consent forms required for account aggregation and linking.",
)
def BankRoutes_account_consent(
    ctx: schemas.BankConsentRequestModel,
) -> schemas.GenericResponse[schemas.EmptyResponse]: ...


@r_BankRoutes.post(
    "/account/setMpin",
    summary="Set UPI PIN",
    description="Initiate the flow to set a new 4 or 6-digit UPI MPIN for a specific bank account.",
)
def BankRoutes_account_setMpin(
    ctx: schemas.SetMpinRequestModel,
) -> schemas.GenericResponse[schemas.EmptyResponse]: ...


@r_BankRoutes.post(
    "/account/changeMpin",
    summary="Change UPI PIN",
    description="Update an existing UPI MPIN by providing the old credentials and new PIN.",
)
def BankRoutes_account_changeMpin(
    ctx: schemas.ChangeMpinCredBlockModel,
) -> schemas.GenericResponse[schemas.EmptyResponse]: ...


@r_BankRoutes.post(
    "/account/checkBalance",
    summary="Check Account Balance",
    description="Securely retrieve the current balance using an encrypted Credential Block.",
)
def BankRoutes_account_checkBalance(
    ctx: schemas.CheckBalanceCredBlockModel,
) -> schemas.GenericResponse[schemas.CheckBalanceResponseModel]: ...


@r_BankRoutes.post(
    "/account/delete",
    summary="Unlink Bank Account",
    description="Remove a linked bank account from the user's UPI profile.",
)
def BankRoutes_account_delete(
    ctx: schemas.RemoveBankAccountRequestModel,
) -> schemas.GenericResponse[schemas.UserAccountModel]: ...


@r_BankRoutes.post(
    "/account/changeDefault",
    summary="Set Default Account",
    description="Set the primary bank account for all incoming and outgoing UPI transactions.",
)
def BankRoutes_account_changeDefault(
    ctx: schemas.ChangeDefaultAccountRequestModel,
) -> schemas.GenericResponse[schemas.UserAccountModel]: ...


@r_BankRoutes.post(
    "/account/generateOTP",
    summary="Request Bank OTP",
    description="Trigger a bank-generated OTP for sensitive operations like resetting an MPIN.",
)
def BankRoutes_account_generateOTP(
    ctx: schemas.GenerateOtpRequestModel,
) -> schemas.GenericResponse[schemas.CredBlockResponse]: ...


@r_BankRoutes.get(
    "/account/list",
    summary="List Linked Accounts",
    description="Retrieve all bank accounts currently linked to the user's profile.",
)
def BankRoutes_account_list(
    bankCode: str,
) -> schemas.GenericResponse[schemas.LinkedBankAccountsResponseModel]: ...


@r_BankRoutes.post(
    "/account/add",
    summary="Add Bank Account",
    description="Link a new bank account by discovering accounts associated with the registered mobile number.",
)
def BankRoutes_account_add(
    ctx: schemas.AddBankAccountRequestModel,
) -> schemas.GenericResponse[schemas.UserAccountsModel]: ...


@r_BankRoutes.post(
    "/lite/add",
    summary="Enable UPI Lite",
    description="Onboard the user to UPI Lite for small-value, PIN-less transactions.",
)
def BankRoutes_lite_add(
    ctx: schemas.UpiLiteOnboardingRequestModel,
) -> schemas.GenericResponse[schemas.UpiLiteOnboardingResponseModel]: ...


@r_BankRoutes.post(
    "/lite/delete",
    summary="Disable UPI Lite",
    description="Deactivate the UPI Lite wallet and refund the remaining balance to the linked bank account.",
)
def BankRoutes_lite_delete() -> (
    schemas.GenericResponse[schemas.UpiLiteSyncResponseModel]
): ...


@r_BankRoutes.post(
    "/lite/sync",
    summary="Sync UPI Lite Balance",
    description="Synchronize local on-device wallet balance with the server-side ledger.",
)
def BankRoutes_lite_sync() -> (
    schemas.GenericResponse[schemas.UpiLiteSyncResponseModel]
): ...


@r_BankRoutes.get(
    "/upiVersions",
    summary="UPI Protocol Versions",
)
def BankRoutes_upiVersions(
    bankCodes: str,
) -> schemas.GenericResponse[schemas.UpiVersionsResponseModel]:
    """
    Check compatible UPI SDK and protocol versions supported by the backend.

    Note: `bankCode` is equal to --

    ```python
    some: list[str] = [...]

    bankCode = ",".join(some[:62])
    ```
    """
    ...


# --- COLLECT ROUTES ---
r_CollectRoutes = APIRouter(prefix="/collectRequest", tags=["Collect Requests"])


@r_CollectRoutes.post(
    "/new",
    summary="Initiate Collect Request",
    description="Create a request to pull funds from a third-party VPA.",
)
def CollectRoutes_new(
    ctx: schemas.TpapCollectCreateRequestModel,
) -> schemas.GenericResponse[schemas.TpapCollectDetailsModel]: ...


@r_CollectRoutes.get(
    "/list",
    summary="List Incoming Requests",
    description="Fetch all pending collect requests sent to the user.",
)
def CollectRoutes_list(
    flow: str = "incoming",
) -> schemas.GenericResponse[schemas.TpapCollectListModel]: ...


@r_CollectRoutes.post(
    "/genCredBlock",
    summary="Generate Payment CredBlock",
    description="Generate the encrypted payload required to authorize a collect request payment.",
)
def CollectRoutes_genCredBlock(
    ctx: schemas.TpapCollectApproveRequestModel,
) -> schemas.GenericResponse[schemas.CredBlockResponse]: ...


@r_CollectRoutes.post(
    "/reject",
    summary="Reject Collect Request",
    description="Decline an incoming payment request from another user or merchant.",
)
def CollectRoutes_reject(
    ctx: schemas.TpapCollectRejectRequestModel,
) -> schemas.GenericResponse[schemas.TpapCollectDetailsModel]: ...


@r_CollectRoutes.post(
    "/approve",
    summary="Approve Collect Request",
    description="Authorize and execute a collect request payment.",
)
def CollectRoutes_approve(
    ctx: schemas.TpapCollectApproveRequestModel,
) -> schemas.GenericResponse[schemas.TpapCollectApproveResponseModel]: ...


@r_CollectRoutes.get(
    "/getOne",
    summary="Get Request Details",
    description="Retrieve full metadata for a specific collect request ID.",
)
def CollectRoutes_getOne(
    crId: str,
) -> schemas.GenericResponse[schemas.TpapCollectDetailsModel]: ...


# --- VPA MANAGEMENT ---
r_CustomVpaRoutes = APIRouter(prefix="/vpa", tags=["VPA Management"])


@r_CustomVpaRoutes.get(
    "/custom/suggestions",
    summary="Get VPA Suggestions",
    description="Generate available custom VPA handles based on user profile data.",
)
def CustomVpaRoutes_custom_suggestions() -> (
    schemas.GenericResponse[schemas.VpaSuggestionsModel]
): ...


@r_CustomVpaRoutes.post(
    "/custom/claim",
    summary="Claim Custom VPA",
    description="Permanently assign a chosen custom VPA handle to the user profile.",
)
def CustomVpaRoutes_custom_claim(
    ctx: schemas.vpaRequestModel,
) -> schemas.GenericResponse[schemas.ClaimVpaResponseModel]: ...


@r_CustomVpaRoutes.get(
    "/list",
    summary="List User VPAs",
    description="Retrieve all Virtual Payment Addresses associated with this user.",
)
def CustomVpaRoutes_list() -> (
    schemas.GenericResponse[schemas.VpasListResponseModel]
): ...


@r_CustomVpaRoutes.get(
    "/custom/status",
    summary="Check VPA Status",
    description="Check if a custom VPA handle is active or pending verification.",
)
def CustomVpaRoutes_custom_status() -> (
    schemas.GenericResponse[schemas.GetCustomVpaStatusModel]
): ...


@r_CustomVpaRoutes.post(
    "/v1/isAvailable",
    summary="Check VPA Availability",
    description="Verify if a specific VPA handle is currently available for registration.",
)
def CustomVpaRoutes_v1_isAvailable(
    ctx: schemas.CustomerVpaRequestModel,
) -> schemas.GenericResponse[schemas.VpaAvailabilityResponseModel]: ...


@r_CustomVpaRoutes.post(
    "/changeDefault",
    summary="Update Primary VPA",
    description="Change which VPA handle is used by default for receiving payments.",
)
def CustomVpaRoutes_changeDefault(
    ctx: schemas.CustomerVpaRequestModel,
) -> schemas.GenericResponse[schemas.UserAccountsModel]: ...


# --- MANDATE ROUTES (RECURRING) ---
r_MandateRoutes = APIRouter(prefix="/mandate", tags=["UPI Mandates"])


@r_MandateRoutes.get(
    "/list",
    summary="List Mandates",
)
def MandateRoutes_list(
    status_filters: str, page_size: int
) -> schemas.GenericResponse[schemas.TpapMandateIncomingListModel]:
    """
    Fetch all recurring payment mandates (active, paused, or revoked).

    status_filters is comma separated values. valid values --

    `success,unpaused,processing,failed,declined,revoked,paused,completed,deemed,pending`
    """
    ...


@r_MandateRoutes.post(
    "/decline",
    summary="Decline Mandate",
    description="Reject an incoming request for a recurring payment mandate.",
)
def MandateRoutes_decline(
    ctx: schemas.TpapMandateRejectRequestModel,
) -> schemas.GenericResponse[schemas.TpapMandateDetailsModel]: ...


@r_MandateRoutes.post(
    "/genCredBlock",
    summary="Generate Mandate CredBlock",
    description="Create the encrypted credential block required to sign a mandate setup.",
)
def MandateRoutes_genCredBlock(
    ctx: schemas.TpapMandateActionRequestModel,
) -> schemas.GenericResponse[schemas.CredBlockResponse]: ...


@r_MandateRoutes.post(
    "/approve",
    summary="Authorize Mandate",
    description="Sign and activate a recurring payment instruction.",
)
def MandateRoutes_approve(
    ctx: schemas.TpapMandateActionRequestModel,
) -> schemas.GenericResponse[schemas.TpapMandateDetailsModel]: ...


@r_MandateRoutes.post(
    "/pause",
    summary="Pause Mandate",
    description="Temporarily stop future payments for an existing mandate.",
)
def MandateRoutes_pause(
    ctx: schemas.TpapMandateActionRequestModel,
) -> schemas.GenericResponse[schemas.TpapMandateDetailsModel]: ...


@r_MandateRoutes.post(
    "/unpause",
    summary="Resume Mandate",
    description="Re-enable a previously paused recurring payment mandate.",
)
def MandateRoutes_unpause(
    ctx: schemas.TpapMandateActionRequestModel,
) -> schemas.GenericResponse[schemas.TpapMandateDetailsModel]: ...


@r_MandateRoutes.post(
    "/revoke",
    summary="Cancel Mandate",
    description="Permanently terminate a mandate instruction.",
)
def MandateRoutes_revoke() -> schemas.GenericResponse[schemas.EmptyResponse]: ...


@r_MandateRoutes.post(
    "/update",
    summary="Modify Mandate",
    description="Update mandate details like validity period or maximum transaction amount.",
)
def MandateRoutes_update(
    ctx: schemas.TpapMandateActionRequestModel,
) -> schemas.GenericResponse[schemas.TpapMandateDetailsModel]: ...


@r_MandateRoutes.post(
    "/createOrder",
    summary="Initialize Mandate Payment",
    description="Create a transaction intent for a specific mandate installment.",
)
def MandateRoutes_createOrder(
    ctx: schemas.TpapCreateMandateRequestModel,
) -> schemas.GenericResponse[schemas.TpapCreateMandateResponseModel]: ...


@r_MandateRoutes.post(
    "/executeOrder",
    summary="Finalize Mandate Payment",
    description="Submit the mandate transaction to the NPCI switch for execution.",
)
def MandateRoutes_executeOrder(
    ctx: schemas.ExecuteMandateCredBlockModel,
) -> schemas.GenericResponse[schemas.TpapCreateMandateResponseModel]: ...


@r_MandateRoutes.get(
    "/getOne",
    summary="Get Mandate Details",
    description="Retrieve detailed configuration for a specific mandate.",
)
def MandateRoutes_getOne() -> schemas.GenericResponse[schemas.EmptyResponse]: ...


@r_MandateRoutes.get(
    "/txn/list",
    summary="Mandate Txn History",
    description="List all transactions processed under a specific mandate ID.",
)
def MandateRoutes_txn_list(
    mandate_id: str,
) -> schemas.GenericResponse[schemas.TpapMandateDetailsModel]: ...


# --- MAPPER ROUTES ---
r_MapperRoutes = APIRouter(tags=["UPI Mapper"])


@r_MapperRoutes.get(
    "/upiMapper/list",
    summary="List Mapped Numbers",
    description="Retrieve mobile-to-VPA mappings stored in the central UPI mapper.",
)
def MapperRoutes_list() -> (
    schemas.GenericResponse[schemas.UpiNumbersWrapperResponse]
): ...


@r_MapperRoutes.post(
    "/upiMapper/new",
    summary="Create Mapper Entry",
    description="Map a mobile number or UPI number to a specific VPA.",
)
def MapperRoutes_new(
    ctx: schemas.CreateUpiNumberRequestModel,
) -> schemas.GenericResponse[schemas.EmptyResponse]: ...


@r_MapperRoutes.post(
    "/upiMapper/update",
    summary="Update Mapper",
    description="Change the destination VPA for a currently mapped mobile number.",
)
def MapperRoutes_update(
    ctx: schemas.UpdateUpiMapperRequestMode,
) -> schemas.GenericResponse[schemas.EmptyResponse]: ...


@r_MapperRoutes.get(
    "/upiNumber/isAvailable",
    summary="Check UPI Number",
    description="Check if a numeric UPI ID is available for registration.",
)
def MapperRoutes_upiNumber_isAvailable() -> (
    schemas.GenericResponse[schemas.EmptyResponse]
): ...


# --- TRANSACTION ROUTES ---
r_TransactionRoutes = APIRouter(prefix="/txn", tags=["Transactions"])


@r_TransactionRoutes.get(
    "/list",
    summary="Transaction History",
    description="Fetch the global transaction history for the user profile.",
)
def TransactionRoutes_list() -> schemas.GenericResponse[schemas.EmptyResponse]: ...


@r_TransactionRoutes.get(
    "/createOrder",
    summary="Initialize Payment",
    description="Create an intent for a new peer-to-peer or peer-to-merchant payment.",
)
def TransactionRoutes_createOrder() -> (
    schemas.GenericResponse[schemas.EmptyResponse]
): ...


@r_TransactionRoutes.get(
    "/executeOrder",
    summary="Execute Payment",
    description="Submit an authorized transaction to the bank for final settlement.",
)
def TransactionRoutes_executeOrder() -> (
    schemas.GenericResponse[schemas.EmptyResponse]
): ...


@r_TransactionRoutes.get(
    "/blockAndSpam",
    summary="Report User",
    description="Block a VPA and report it as a spam/fraudulent account to NPCI.",
)
def TransactionRoutes_blockAndSpam() -> (
    schemas.GenericResponse[schemas.EmptyResponse]
): ...


# --- UDIR (DISPUTES) ---
r_UDIRRoutes = APIRouter(prefix="/udir", tags=["Dispute Management"])


@r_UDIRRoutes.get(
    "/create",
    summary="Raise Dispute",
    description="Initiate a UDIR (Unified Dispute and Issue Resolution) complaint for a failed transaction.",
)
def UDIRRoutes_create() -> schemas.GenericResponse[schemas.EmptyResponse]: ...


@r_UDIRRoutes.get(
    "/status",
    summary="Check Dispute Status",
    description="Track the progress of an active UDIR dispute case.",
)
def UDIRRoutes_status() -> schemas.GenericResponse[schemas.EmptyResponse]: ...


# --- DELEGATE (LINKED ACCOUNTS) ---
r_UpiDelegateRoutes = APIRouter(prefix="/delegate", tags=["Delegate Accounts"])


@r_UpiDelegateRoutes.get(
    "/link/remainingLimit",
    summary="Get Delegate Limits",
    description="Check the spending limit remaining for a delegated/child account.",
)
def UpiDelegateRoutes_link_remainingLimit() -> (
    schemas.GenericResponse[schemas.EmptyResponse]
): ...


@r_UpiDelegateRoutes.get(
    "/payRequest/generateCredBlock",
    summary="Delegate CredBlock",
    description="Generate credentials for a delegate user to sign a payment.",
)
def UpiDelegateRoutes_payRequest_generateCredBlock() -> (
    schemas.GenericResponse[schemas.EmptyResponse]
): ...


@r_UpiDelegateRoutes.get(
    "/payRequest/",
    summary="Get Delegate Requests",
    description="Fetch all payment requests waiting for parent approval.",
)
def UpiDelegateRoutes_payRequest() -> (
    schemas.GenericResponse[schemas.EmptyResponse]
): ...


@r_UpiDelegateRoutes.get(
    "/payRequest/approve",
    summary="Parent Approval",
    description="Authorize a payment request initiated by a delegate account.",
)
def UpiDelegateRoutes_payRequest_approve() -> (
    schemas.GenericResponse[schemas.EmptyResponse]
): ...


@r_UpiDelegateRoutes.get(
    "/payRequest/decline",
    summary="Parent Decline",
    description="Reject a payment request initiated by a delegate account.",
)
def UpiDelegateRoutes_payRequest_decline() -> (
    schemas.GenericResponse[schemas.EmptyResponse]
): ...


# --- USER & SECURITY ---
r_UserRoutes = APIRouter(prefix="/user", tags=["User & Security"])


@r_UserRoutes.get(
    "/v1/getAuthSession",
    summary="Get Auth Session",
    description="Retrieve a fresh authentication session for the native UPI SDK.",
)
def UserRoutes_v1_getAuthSession() -> (
    schemas.GenericResponse[schemas.EmptyResponse]
): ...


@r_UserRoutes.get(
    "/getAccInfo",
    summary="User Account Info",
    description="Fetch general user profile metadata and registration status.",
)
def UserRoutes_getAccInfo() -> schemas.GenericResponse[schemas.EmptyResponse]: ...


@r_UserRoutes.get(
    "/generateSimBinding",
    summary="Initiate Device Binding",
    description="Start the SIM binding process by generating a unique challenge for SMS verification.",
)
def UserRoutes_generateSimBinding() -> (
    schemas.GenericResponse[schemas.EmptyResponse]
): ...


@r_UserRoutes.get(
    "/verifySimBinding",
    summary="Verify Device Binding",
    description="Confirm the SMS challenge to cryptographically bind the device to the user account.",
)
def UserRoutes_verifySimBinding() -> schemas.GenericResponse[schemas.EmptyResponse]: ...


@r_UserRoutes.get(
    "/fetchNPCIToken",
    summary="Fetch NPCI Token",
    description="Retrieve the short-lived security token required for NPCI common library interactions.",
)
def UserRoutes_fetchNPCIToken() -> schemas.GenericResponse[schemas.EmptyResponse]: ...


@r_UserRoutes.get(
    "/deRegister",
    summary="De-register UPI",
    description="Permanently wipe the UPI profile and device bindings for this user.",
)
def UserRoutes_deRegister() -> schemas.GenericResponse[schemas.EmptyResponse]: ...


@r_UserRoutes.get(
    "/genCredBlock",
    summary="Global CredBlock",
    description="Generate a generic credential block for miscellaneous secure operations.",
)
def UserRoutes_genCredBlock() -> schemas.GenericResponse[schemas.EmptyResponse]: ...


# --- VPA VERIFICATION ---
r_VpaVerifyRoutes = APIRouter(prefix="/vpa", tags=["VPA Verification"])


@r_VpaVerifyRoutes.post(
    "/verify",
    summary="Verify VPA",
    description="Perform a real-time check against the NPCI mapper to fetch the name of a VPA owner.",
)
def VpaVerifyRoutes_verify(
    ctx: schemas.VerifyVpaRequestModel,
) -> schemas.GenericResponse[schemas.EmptyResponse]: ...


@r_VpaVerifyRoutes.get(
    "/verifyExt",
    summary="External VPA Verification",
    description="Extended verification for cross-PSP VPA handles.",
)
def VpaVerifyRoutes_verifyExt() -> schemas.GenericResponse[schemas.EmptyResponse]: ...


# Include all routers
for name, router in locals().copy().items():
    if name.startswith("r_"):
        app.include_router(router)
