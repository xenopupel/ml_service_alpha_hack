from src.processing.abstracts.tree_classes import Node
from src.utils.enums import RecOutputs
from typing import Any


class SmsFailureNode(Node):
    def do_process(self, data: Any) -> Any:
        return RecOutputs.PAY_CONTROL.value
