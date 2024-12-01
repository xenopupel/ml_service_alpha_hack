from src.processing.abstracts.tree_classes import Processor
from src.processing.nodes.usecase import UseCaseSwitch
from src.processing.nodes.old_new_nodes import NewUserNode, PredictionNode, OldNewSwitch
from src.ml_model.predict import ModelPredictor
from src.processing.nodes.rooting_node import RootingNode
from src.processing.nodes.sms_failure_node import SmsFailureNode
from src.utils.enums import UseCaseType

def get_processor():
    predictor = ModelPredictor('src/ml_model/trained_models/model_stub.cbm')

    # Для обработки новый/старый user
    new_user_node = NewUserNode()
    existing_user_node = PredictionNode(model_predictor=predictor)
    old_new_switch = OldNewSwitch({
        True: new_user_node,
        False: existing_user_node,
    })

    # Перевод денег или подпись базового документа
    base_money_node = RootingNode(switch=old_new_switch)

    # Перевод крупных сумм денег или подпись важного документа
    big_money_node = RootingNode(switch=old_new_switch)

    # Переход во вкладку изменений способов подтверждения
    change_method_node = PredictionNode(model_predictor=predictor)

    # Сломанное смс - рекомендуем приложение
    sms_failure_node = SmsFailureNode()

    # Обработка use кейсов
    usecase_switch = UseCaseSwitch({
        UseCaseType.BASE_OPERATION.value: base_money_node,
        UseCaseType.BIG_OPERATION.value: big_money_node,
        UseCaseType.CHANGE_SIGNATURE_METHOD.value: change_method_node,
        UseCaseType.SMS_FAILURE.value: sms_failure_node,
    })

    # Входная нода
    entry_node = RootingNode(switch=usecase_switch)
    entry_node.do_process = lambda data: data

    return Processor(initial_node=entry_node)