from pydantic import BaseModel
from typing import List, Literal

class SignatureCounts(BaseModel):
    mobile: int  # Количество подписанных документов в мобайле
    web: int     # Количество подписанных документов в вебе

class Signatures(BaseModel):
    common: SignatureCounts  # Базовые документы
    special: SignatureCounts  # Документы особой важности

class InputData(BaseModel):
    clientId: str  # ИД пользователя
    organizationId: str  # ИД организации
    segment: Literal["Малый бизнес", "Средний бизнес", "Крупный бизнес"]  # Сегмент организации
    role: Literal["ЕИО", "Сотрудник"]  # Роль уполномоченного лица
    organizations: int  # Общее количество организаций
    currentMethod: Literal["SMS", "PayControl", "QDSToken", "QDSMobile"]  # Действующий способ подписания
    mobileApp: bool  # Наличие мобильного приложения
    signatures: Signatures  # Подписанные ранее типы документов
    availableMethods: List[Literal["SMS", "PayControl", "QDSToken", "QDSMobile"]]  # Уже подключенные способы подписания
    claims: int  # Наличие обращений в банк

class OutputData(BaseModel):
    model_output: Literal["PayControl", "QDSToken", "QDSMobile"]