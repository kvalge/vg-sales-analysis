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
