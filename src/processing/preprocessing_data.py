def preprocess_data(data, is_new = True, usecase='base_money'):
    data = data.copy()
    data['is_new'] = is_new
    data['usecase'] = usecase
    return data
