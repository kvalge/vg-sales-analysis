from data.load_data import load_data

data = load_data()

def top7_na_sales_by_group(df, group_field):
    return (
        df.groupby(group_field, as_index=False)['NA Sales']
        .sum()
        .sort_values(by='NA Sales', ascending=False)
        .head(7)
        .round(2)
        .to_dict(orient='records')
    )

def get_sales_data_for_period(start_year, end_year):
    df = data[(data['Year'] >= start_year) & (data['Year'] <= end_year)]
    genres = top7_na_sales_by_group(df, 'Genre')
    publishers = top7_na_sales_by_group(df, 'Publisher')
    return genres, publishers