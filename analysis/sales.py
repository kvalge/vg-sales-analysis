from data.load_data import load_data

data = load_data()


def sales_by_year():
    sales = data.groupby('Year')[['NA Sales', 'EU Sales', 'JP Sales', 'Other Sales', 'Global Sales']].sum()
    sales = sales.round(2)
    total_per_year = data.groupby('Year').size()
    sales['Total Games'] = total_per_year
    sales_dict = sales.reset_index().to_dict(orient='records')

    totals = sales[['NA Sales', 'EU Sales', 'JP Sales', 'Other Sales', 'Global Sales', 'Total Games']].sum().round(
        2).to_dict()
    totals['Year'] = 'Total'

    return sales_dict, totals


def sales_by_publisher():
    sales = data.groupby('Publisher')[['NA Sales', 'EU Sales', 'JP Sales', 'Other Sales', 'Global Sales']].sum()
    sales = sales.round(2)
    top_sales = sales.sort_values(by='Global Sales', ascending=False).head(10)
    return top_sales.reset_index().to_dict(orient='records')


def sales_by_genre():
    sales = data.groupby('Genre')[['NA Sales', 'EU Sales', 'JP Sales', 'Other Sales', 'Global Sales']].sum()
    sales = sales.round(2)
    top_sales = sales.sort_values(by='Global Sales', ascending=False)
    return top_sales.reset_index().to_dict(orient='records')


def na_sales_by_genre_over_time():
    grouped = data.groupby(['Year', 'Genre'])['NA Sales'].sum().unstack().fillna(0)
    grouped = grouped.round(2)
    return grouped


def na_sales_by_top_publishers_action_games():
    filtered_data = data[data['Genre'] == 'Action']
    sales = (
        filtered_data.groupby('Publisher')['NA Sales']
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .round(2)
    )

    sales_data = sales.reset_index()
    sales_data.columns = ['Publisher', 'NA Sales']
    return sales_data.to_dict(orient='records')


def na_sales_by_top_20_action_games():
    filtered_data = data[data['Genre'] == 'Action']

    top_20 = (
        filtered_data
        .groupby(['Name', 'Publisher'], as_index=False)['NA Sales']
        .sum()
        .sort_values(by='NA Sales', ascending=False)
        .head(20)
        .round(2)
    )

    return top_20.to_dict(orient='records')


def na_sales_by_genre_2006_2011():
    df = data[(data['Year'] >= 2006) & (data['Year'] <= 2011)]
    by_genre_from_2006_to_2011 = (
        df
        .groupby(['Genre'], as_index=False)['NA Sales']
        .sum()
        .sort_values(by='NA Sales', ascending=False)
        .round(2)
    )
    return by_genre_from_2006_to_2011.to_dict(orient='records')


