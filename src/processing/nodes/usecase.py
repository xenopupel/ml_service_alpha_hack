from src.processing.abstracts.tree_classes import Node, Switch
from src.processing.nodes.no_recommended_node import NoRecommendedNode
from typing import Any, Optional


class UseCaseSwitch(Switch):
    def __init__(self, node_mapping: dict):
        self.node_mapping = node_mapping

    def get_next_node(self, data: Any) -> Optional[Node]:
        if isinstance(data, dict) and 'usecase' in data:
            usecase = data['usecase']
            node = self.node_mapping.get(usecase)
            if node:
                return node
            else:
                print(f"Неизвестный usecase: {usecase}")
                exit_node = NoRecommendedNode()
                return exit_node
        else:
            print("Поле 'usecase' отсутствует в данных или данные не являются словарем")
        exit_node = NoRecommendedNode()
        return exit_node