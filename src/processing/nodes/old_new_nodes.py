from src.processing.abstracts.tree_classes import Node, Switch
from src.ml_model.predict import ModelPredictor
from typing import Any, Optional


class NewUserNode(Node):
    def do_process(self, data: Any) -> Any:
        if data['usecase'] == 'base_money':
            return 'PayControl'
        elif data['usecase'] == 'big_money':
            return 'QDSToken'


class PredictionNode(Node):
    def __init__(self, model_predictor: ModelPredictor, switch: Optional['Switch'] = None):
        super().__init__(switch)
        self.model_predictor = model_predictor 

    def do_process(self, data: Any) -> Any:
        prediction = self.model_predictor.predict(data)
        return prediction


class OldNewSwitch(Switch):
    def __init__(self, node_mapping: dict):
        self.node_mapping = node_mapping

    def get_next_node(self, data: Any) -> Optional[Node]:
        if isinstance(data, dict) and 'is_new' in data:
            is_new = data['is_new']
            node = self.node_mapping.get(is_new)
            if node:
                return node
        else:
            print("Поле 'is_new' отсутствует в данных или данные не являются словарем")
        return None
