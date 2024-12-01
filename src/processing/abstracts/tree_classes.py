from abc import ABC, abstractmethod
from typing import Any, Optional


class Node(ABC):
    def __init__(self, switch: Optional['Switch'] = None):
        self.switch = switch

    def process(self, data: Any) -> Any:
        data = self.do_process(data)
        if self.switch:
            next_node = self.switch.get_next_node(data)
            if next_node:
                return next_node.process(data)
        return data

    @abstractmethod
    def do_process(self, data: Any) -> Any:
        pass


class Switch(ABC):
    @abstractmethod
    def get_next_node(self, data: Any) -> Optional[Node]:
        pass


class Processor:
    def __init__(self, initial_node: Node):
        self.initial_node = initial_node

    def process(self, data: Any) -> Any:
        return self.initial_node.process(data)