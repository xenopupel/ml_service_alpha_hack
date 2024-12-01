import pytest
from src.processing.nodes.old_new_nodes import NewUserNode, PredictionNode
from src.api.contracts import InputData, Signatures, SignatureCounts
from src.ml_model.predict import ModelPredictor 

class TestNewUserNode:
    def test_do_process_base_money(self):
        """Test NewUserNode with 'base_money' usecase."""
        node = NewUserNode()
        data = {'usecase': 'base_money'}
        result = node.do_process(data)
        assert result == 'PayControl'

    def test_do_process_big_money(self):
        """Test NewUserNode with 'big_money' usecase."""
        node = NewUserNode()
        data = {'usecase': 'big_money'}
        result = node.do_process(data)
        assert result == 'QDSToken'

    def test_do_process_unknown_usecase(self):
        """Test NewUserNode with an unknown usecase."""
        node = NewUserNode()
        data = {'usecase': 'unknown'}
        result = node.do_process(data)
        assert result is None

class TestPredictionNode:
    def test_do_process(self):
        """Test PredictionNode with real ModelPredictor."""
        predictor = ModelPredictor('src/ml_model/trained_models/model_stub.cbm') 
        node = PredictionNode(model_predictor=predictor)

        data = InputData(
            clientId='client123',
            organizationId='org456',
            segment='Малый бизнес',
            role='ЕИО',
            organizations=3,
            currentMethod='SMS',
            mobileApp=True,
            signatures=Signatures(
                common=SignatureCounts(mobile=5, web=10),
                special=SignatureCounts(mobile=2, web=3)
            ),
            availableMethods=['SMS', 'PayControl'],
            claims=1
        ).model_dump() 

        result = node.do_process(data)
        allowed_methods = ['PayControl', 'QDSMobile', 'QDSToken']
        assert result in allowed_methods, f"Unexpected recommended method: {result}"
