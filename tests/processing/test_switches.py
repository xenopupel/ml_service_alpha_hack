import pytest
from src.processing.nodes.usecase import UseCaseSwitch
from src.processing.nodes.old_new_nodes import OldNewSwitch
from src.processing.abstracts.tree_classes import Node
from src.processing.nodes.no_recommended_node import NoRecommendedNode
from src.utils.enums import UseCaseType

# Define simple test nodes
class TestNode(Node):
    def __init__(self, name):
        self.name = name

    def do_process(self, data):
        return f"Processed by {self.name}"

    def __eq__(self, other):
        return isinstance(other, TestNode) and self.name == other.name


class TestOldNewSwitch:
    @pytest.fixture(autouse=True)
    def setup(self):
        # Initialize real nodes instead of mocks
        self.true_node = TestNode('TrueNode')
        self.false_node = TestNode('FalseNode')
        self.switch = OldNewSwitch({
            True: self.true_node,
            False: self.false_node
        })

    def test_get_next_node_true(self):
        """Test OldNewSwitch with 'is_new' == True."""
        data = {'is_new': True}
        result = self.switch.get_next_node(data)
        assert result == self.true_node

    def test_get_next_node_false(self):
        """Test OldNewSwitch with 'is_new' == False."""
        data = {'is_new': False}
        result = self.switch.get_next_node(data)
        assert result == self.false_node

    def test_get_next_node_missing_key(self, capsys):
        """Test OldNewSwitch with missing 'is_new' key."""
        data = {'other_key': 'value'}
        result = self.switch.get_next_node(data)
        assert result is None
        captured = capsys.readouterr()
        assert "Поле 'is_new' отсутствует в данных или данные не являются словарем" in captured.out

    def test_get_next_node_invalid_data(self, capsys):
        """Test OldNewSwitch with invalid data type."""
        data = 'invalid_data'
        result = self.switch.get_next_node(data)
        assert result is None
        captured = capsys.readouterr()
        assert "Поле 'is_new' отсутствует в данных или данные не являются словарем" in captured.out

class TestUseCaseSwitch:
    @pytest.fixture(autouse=True)
    def setup(self):
        # Initialize real nodes instead of mocks
        self.base_money_node = TestNode('BaseMoneyNode')
        self.big_money_node = TestNode('BigMoneyNode')
        self.change_method_node = TestNode('ChangeMethodNode')
        self.no_recommendation_node = NoRecommendedNode()
        self.switch = UseCaseSwitch(
            node_mapping={
                'base_money': self.base_money_node,
                'big_money': self.big_money_node,
                'change_signature_method': self.change_method_node
            }
        )

    def test_get_next_node_base_money(self):
        """Test UseCaseSwitch with 'base_money' usecase."""
        data = {'usecase': UseCaseType.BASE_OPERATION.value}
        result = self.switch.get_next_node(data)
        assert result == self.base_money_node

    def test_get_next_node_big_money(self):
        """Test UseCaseSwitch with 'big_money' usecase."""
        data = {'usecase': 'big_money'}
        result = self.switch.get_next_node(data)
        assert result == self.big_money_node

    def test_get_next_node_change_method(self):
        """Test UseCaseSwitch with 'change_signature_method' usecase."""
        data = {'usecase': 'change_signature_method'}
        result = self.switch.get_next_node(data)
        assert result == self.change_method_node

    def test_get_next_node_unknown_usecase(self, capsys):
        """Test UseCaseSwitch with an unknown usecase."""
        data = {'usecase': 'unknown'}
        result = self.switch.get_next_node(data)
        assert isinstance(result, NoRecommendedNode) 
        captured = capsys.readouterr()
        assert "Неизвестный usecase: unknown" in captured.out

    def test_get_next_node_missing_key(self, capsys):
        """Test UseCaseSwitch with missing 'usecase' key."""
        data = {'other_key': 'value'}
        result = self.switch.get_next_node(data)
        assert isinstance(result, NoRecommendedNode) 
        captured = capsys.readouterr()
        assert "Поле 'usecase' отсутствует в данных или данные не являются словарем" in captured.out
