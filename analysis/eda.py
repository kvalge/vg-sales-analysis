from io import StringIO

from data.load_data import load_data

data = load_data()

def get_shape():
    return {'rows': data.shape[0], 'columns': data.shape[1]}

def get_info():
    buffer = StringIO()
    data.info(buf=buffer)
    info_str = buffer.getvalue()
    return info_str.splitlines()


def get_describe():
    float_columns = data.select_dtypes(include=['float64'])
    return float_columns.describe().transpose().to_dict(orient='index')

def get_head():
    buffer = StringIO()
    buffer.write(data.head().to_string())
    head_str = buffer.getvalue()
    return head_str.splitlines()

def get_unique_counts():
    unique_counts = {
        'Name': len(data['Name'].unique()),
        'Platform': len(data['Platform'].unique()),
        'Genre': len(data['Genre'].unique()),
        'Publisher': len(data['Publisher'].unique())
    }
    return unique_counts




