from enum import Enum

class UseCaseType(Enum):
    BASE_OPERATION = 'base_operation_signature'
    BIG_OPERATION = 'big_operation_signature'
    CHANGE_SIGNATURE_METHOD = 'change_signature_method'
    SMS_FAILURE = 'sms_failure'

class RecOutputs(Enum):
    PAY_CONTROL = 'PayControl'
    QDS_TOKEN = 'QDSToken'
    QDS_MOBILE = 'QDSMobile'
    NO_RECOMMENDATION = 'NoRecommendedMethod'