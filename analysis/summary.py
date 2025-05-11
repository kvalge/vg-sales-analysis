from io import StringIO
from data.load_data import load_data

data = load_data()


def already_logged(identifier: str) -> bool:
    try:
        with open('data/summary.txt', 'r') as file:
            contents = file.read()
            return identifier in contents
    except FileNotFoundError:
        return False


def get_shape():
    shape = {'rows': data.shape[0], 'columns': data.shape[1]}
    identifier = f"No of rows: {shape['rows']}, No of columns: {shape['columns']}"

    if not already_logged(identifier):
        with open('data/summary.txt', 'a') as file:
            file.write(f"{identifier}\n\n")
    return shape


def get_info():
    buffer = StringIO()
    data.info(buf=buffer)
    info_str = buffer.getvalue()
    identifier = info_str.strip().splitlines()[0]

    if not already_logged(identifier):
        with open('data/summary.txt', 'a') as file:
            file.write(info_str + '\n\n')

    return info_str.splitlines()


def get_describe():
    float_columns = data.select_dtypes(include=['float64'])
    describe_str = float_columns.describe().transpose().to_string()
    identifier = describe_str.splitlines()[0].strip()

    if not already_logged(identifier):
        with open('data/summary.txt', 'a') as file:
            file.write(describe_str + '\n\n')

    return float_columns.describe().transpose().to_dict(orient='index')


def get_head():
    head_str = data.head().to_string()
    identifier = head_str.splitlines()[0].strip()

    if not already_logged(identifier):
        with open('data/summary.txt', 'a') as file:
            file.write(head_str + '\n\n')

    return head_str.splitlines()


def get_unique_counts():
    unique_counts = {
        'Name': len(data['Name'].unique()),
        'Platform': len(data['Platform'].unique()),
        'Genre': len(data['Genre'].unique()),
        'Publisher': len(data['Publisher'].unique())
    }

    identifier = f"Name: {unique_counts['Name']}"

    if not already_logged(identifier):
        with open('data/summary.txt', 'a') as file:
            file.write("Summary\n\n")
            file.write("Column Descriptions:\n")
            file.write("Name: The game's name\n")
            file.write("Platform: Platform of the game's release (i.e. PC, PS4, etc.)\n")
            file.write("Year: Year of the game's release\n")
            file.write("Genre: Genre of the game\n")
            file.write("Publisher: Publisher of the game\n")
            file.write("NA Sales: Sales in North America (in millions)\n")
            file.write("EU Sales: Sales in Europe (in millions)\n")
            file.write("JP Sales: Sales in Japan (in millions)\n")
            file.write("Other Sales: Sales in the rest of the world (in millions)\n")
            file.write("Global Sales: Total worldwide sales\n\n")
            file.write("Unique counts:\n")
            for key, value in unique_counts.items():
                file.write(f'{key}: {value}\n')
            file.write('\n')

    return unique_counts
