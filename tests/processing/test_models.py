import pytest
from pydantic import ValidationError
from src.api.contracts import InputData, OutputData, Signatures, SignatureCounts

class TestInputDataValidation:
    def test_valid_input_data(self):
        """Test that valid InputData does not raise ValidationError."""
        try:
            InputData(
                clientId='client_valid',
                organizationId='org_valid',
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
            )
        except ValidationError:
            pytest.fail("InputData raised ValidationError unexpectedly!")

    def test_invalid_segment(self):
        """Test that invalid 'segment' raises ValidationError."""
        with pytest.raises(ValidationError):
            InputData(
                clientId='client_invalid',
                organizationId='org_invalid',
                segment='Invalid Segment',
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
            )

class TestOutputDataValidation:
    def test_valid_output_data(self):
        """Test that valid OutputData does not raise ValidationError."""
        try:
            OutputData(recommendedMethod='PayControl')
        except ValidationError:
            pytest.fail("OutputData raised ValidationError unexpectedly!")

    def test_invalid_recommended_method(self):
        """Test that invalid 'recommendedMethod' raises ValidationError."""
        with pytest.raises(ValidationError):
            OutputData(recommendedMethod='InvalidMethod')
