from data.load_data import load_data
import matplotlib.pyplot as plt

data = load_data()

def get_name_histogram():
    counts = data['Name'].value_counts().head(30)
    plt.figure(figsize=(12, 8))
    names = counts.index
    counts = counts.values
    plt.bar(names, counts, color='#89899a', width=0.9)
    plt.title('Top 30 Game Frequency')
    plt.xlabel('Name')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('static/charts/names_histogram.png')
    plt.close()


def get_platform_histogram():
    counts = data['Platform'].value_counts()
    plt.figure(figsize=(12, 8))
    names = counts.index
    counts = counts.values
    plt.bar(names, counts, color='#89899a', width=0.9)
    plt.title('Platform Frequency')
    plt.xlabel('Platform')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('static/charts/platforms_histogram.png')
    plt.close()

def get_genre_histogram():
    counts = data['Genre'].value_counts()
    plt.figure(figsize=(12, 8))
    names = counts.index
    counts = counts.values
    plt.bar(names, counts, color='#89899a', width=0.9)
    plt.title('Genre Frequency')
    plt.xlabel('Genre')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('static/charts/genres_histogram.png')
    plt.close()

def get_publisher_histogram():
    counts = data['Publisher'].value_counts().head(30)
    plt.figure(figsize=(12, 8))
    names = counts.index
    counts = counts.values
    plt.bar(names, counts, color='#89899a', width=0.9)
    plt.title('Top 30 Publisher Frequency')
    plt.xlabel('Publisher')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('static/charts/publishers_histogram.png')
    plt.close()


def get_sales_by_year_linechart():
    sales = data.groupby('Year')[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']].sum()
    sales = sales.round(2)

    plt.figure(figsize=(10, 6))
    for column in sales.columns:
        plt.plot(sales.index, sales[column], label=column)

    plt.xlabel('Year')
    plt.ylabel('Sales (in millions)')
    plt.title('Sales by Year')
    plt.legend()

    plt.tight_layout()

    plt.savefig('static/charts/sales_by_year.png')
    plt.close()

def get_sales_by_publisher_barchart():
    sales = data.groupby('Publisher')[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']].sum()
    sales = sales.round(2)
    sales = sales.sort_values(by='Global_Sales', ascending=False).head(10)

    publishers = sales.index.tolist()
    x = range(len(publishers))

    width = 0.15
    plt.figure(figsize=(10, 6))

    # Global Sales on esimene (nihke vasakule 2x)
    plt.bar([i - 2 * width for i in x], sales['Global_Sales'], width=width, label='Global Sales')
    plt.bar([i - width for i in x], sales['NA_Sales'], width=width, label='NA Sales')
    plt.bar(x, sales['EU_Sales'], width=width, label='EU Sales')
    plt.bar([i + width for i in x], sales['JP_Sales'], width=width, label='JP Sales')
    plt.bar([i + 2 * width for i in x], sales['Other_Sales'], width=width, label='Other Sales')

    plt.xticks(x, publishers, rotation=45, ha='right')
    plt.xlabel('Publisher')
    plt.ylabel('Sales (in millions)')
    plt.title('Top 10 Publishers by Sales')
    plt.legend()
    plt.tight_layout()

    plt.savefig('static/charts/sales_by_publisher.png')
    plt.close()

