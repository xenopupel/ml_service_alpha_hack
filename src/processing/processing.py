from src.processing.abstracts.tree_classes import Node, Switch, Processor
from src.processing.nodes.usecase import UseCaseSwitch
from src.processing.nodes.old_new_nodes import NewUserNode, PredictionNode, OldNewSwitch
from src.ml_model.predict import ModelPredictor
from src.processing.nodes.rooting_node import RootingNode
from typing import Any, Optional


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

    # Обработка use кейсов
    usecase_switch = UseCaseSwitch({
        'base_money': base_money_node,
        'big_money': big_money_node,
        'change_signature_method': change_method_node
    })

    # Входная нода
    entry_node = RootingNode(switch=usecase_switch)
    entry_node.do_process = lambda data: data

    return Processor(initial_node=entry_node)