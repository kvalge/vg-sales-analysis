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
    return data.describe(include='all').transpose().to_dict(orient='index')

def get_head():
    df = load_data()
    buffer = StringIO()
    buffer.write(df.head().to_string())
    head_str = buffer.getvalue()
    return head_str.splitlines()




