from src.utils.enums import UseCaseType

def preprocess_data(data, is_new = True, usecase=UseCaseType.BASE_OPERATION.value):
    data = data.copy()
    data['is_new'] = is_new
    data['usecase'] = usecase
    return data
