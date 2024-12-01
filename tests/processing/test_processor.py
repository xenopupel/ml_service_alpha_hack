import pytest
from src.api.contracts import InputData, Signatures, SignatureCounts
from src.processing.processing import get_processor  # Adjust the import to your actual module

class TestProcessor:
    @pytest.mark.parametrize(
        "input_data, extra_fields",
        [
            (
                InputData(
                    clientId='client1',
                    organizationId='org1',
                    segment='Малый бизнес',
                    role='ЕИО',
                    organizations=1,
                    currentMethod='SMS',
                    mobileApp=True,
                    signatures=Signatures(
                        common=SignatureCounts(mobile=0, web=0),
                        special=SignatureCounts(mobile=0, web=0)
                    ),
                    availableMethods=['SMS'],
                    claims=0
                ).model_dump(),
                {'is_new': True, 'usecase': 'base_money'}
            ),
            (
                InputData(
                    clientId='client2',
                    organizationId='org2',
                    segment='Средний бизнес',
                    role='Сотрудник',
                    organizations=2,
                    currentMethod='PayControl',
                    mobileApp=False,
                    signatures=Signatures(
                        common=SignatureCounts(mobile=5, web=15),
                        special=SignatureCounts(mobile=2, web=5)
                    ),
                    availableMethods=['SMS', 'PayControl'],
                    claims=2
                ).model_dump(),
                {'is_new': False, 'usecase': 'big_money'}
            ),
            (
                InputData(
                    clientId='client3',
                    organizationId='org3',
                    segment='Крупный бизнес',
                    role='ЕИО',
                    organizations=5,
                    currentMethod='QDSToken',
                    mobileApp=True,
                    signatures=Signatures(
                        common=SignatureCounts(mobile=10, web=20),
                        special=SignatureCounts(mobile=5, web=10)
                    ),
                    availableMethods=['QDSToken', 'PayControl'],
                    claims=5
                ).model_dump(),
                {'usecase': 'change_signature_method'}
            ),
            (
                InputData(
                    clientId='client4',
                    organizationId='org4',
                    segment='Малый бизнес',
                    role='Сотрудник',
                    organizations=1,
                    currentMethod='SMS',
                    mobileApp=False,
                    signatures=Signatures(
                        common=SignatureCounts(mobile=0, web=0),
                        special=SignatureCounts(mobile=0, web=0)
                    ),
                    availableMethods=['SMS'],
                    claims=0
                ).model_dump(),
                {'usecase': 'unknown'}
            )
        ],
        ids=[
            "NewUser_BaseMoney",
            "ExistingUser_BigMoney",
            "ChangeSignatureMethod",
            "UnknownUseCase"
        ]
    )
    def test_processor_flow(self, input_data, extra_fields):
        """Test the processor outputs valid recommended methods."""
        processor = get_processor()
        data = input_data.copy()
        data.update(extra_fields)
        result = processor.process(data)

        # Define the set of allowed outputs
        allowed_methods = ['PayControl', 'QDSMobile', 'QDSToken', 'NoRecommendedMethod']

        assert result in allowed_methods, f"Unexpected recommended method: {result}"
