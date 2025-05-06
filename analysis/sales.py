from data.load_data import load_data

data = load_data()

def sales_by_year():
    sales = data.groupby('Year')[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']].sum()
    sales = sales.round(2)
    return sales.reset_index().to_dict(orient='records')

def sales_by_publisher():
    sales = data.groupby('Publisher')[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']].sum()
    sales = sales.round(2)
    top_sales = sales.sort_values(by='Global_Sales', ascending=False).head(10)
    return top_sales.reset_index().to_dict(orient='records')
