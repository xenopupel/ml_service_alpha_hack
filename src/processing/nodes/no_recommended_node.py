from src.processing.abstracts.tree_classes import Node
from typing import Any


class NoRecommendedNode(Node):
    def do_process(self, data: Any) -> Any:
        return 'NoRecommendedMethod'
