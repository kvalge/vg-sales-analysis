from data.load_data import load_data
import matplotlib.pyplot as plt

data = load_data()


def generate_histogram(column, title, xlabel, ylabel, top_n=None, figsize=(12, 8), color='#89899a', width=0.9):
    counts = data[column].value_counts()
    if top_n:
        counts = counts.head(top_n)

    plt.figure(figsize=figsize)
    names = counts.index
    counts = counts.values
    plt.bar(names, counts, color=color, width=width)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(f'static/charts/{column.lower()}_histogram.png')
    plt.close()


def get_name_histogram():
    generate_histogram(
        column='Name',
        title='Top 30 Game Frequency',
        xlabel='Name',
        ylabel='Frequency',
        top_n=30
    )


def get_platform_histogram():
    generate_histogram(
        column='Platform',
        title='Platform Frequency',
        xlabel='Platform',
        ylabel='Frequency'
    )


def get_genre_histogram():
    generate_histogram(
        column='Genre',
        title='Genre Frequency',
        xlabel='Genre',
        ylabel='Frequency'
    )


def get_publisher_histogram():
    generate_histogram(
        column='Publisher',
        title='Top 30 Publisher Frequency',
        xlabel='Publisher',
        ylabel='Frequency',
        top_n=30
    )


def get_sales_by_year_linechart():
    sales = data.groupby('Year')[['NA Sales', 'EU Sales', 'JP Sales', 'Other Sales', 'Global Sales']].sum()
    sales = sales.round(2)

    plt.figure(figsize=(10, 6))
    plt.plot(sales.index, sales['NA Sales'], label='NA Sales', color='darkblue')
    plt.plot(sales.index, sales['EU Sales'], label='EU Sales', color='firebrick')
    plt.plot(sales.index, sales['JP Sales'], label='JP Sales', color='orange')
    plt.plot(sales.index, sales['Other Sales'], label='Other Sales', color='gold')
    plt.plot(sales.index, sales['Global Sales'], label='Global Sales', color='silver')

    plt.xlabel('Year')
    plt.ylabel('Sales (in millions)')
    plt.title('Sales by Year')
    plt.legend()

    plt.xticks(sales.index, rotation=45, ha='right')
    plt.tight_layout()

    plt.savefig('static/charts/sales_by_year.png')
    plt.close()


def get_sales_by_publisher_barchart():
    sales = data.groupby('Publisher')[['NA Sales', 'EU Sales', 'JP Sales', 'Other Sales', 'Global Sales']].sum()
    sales = sales.round(2)
    sales = sales.sort_values(by='Global Sales', ascending=False).head(10)

    publishers = sales.index.tolist()
    x = range(len(publishers))

    width = 0.15
    plt.figure(figsize=(10, 6))

    plt.bar([i - 2 * width for i in x], sales['Global Sales'], width=width, label='Global Sales', color='silver')
    plt.bar([i - width for i in x], sales['NA Sales'], width=width, label='NA Sales', color='darkblue')
    plt.bar(x, sales['EU Sales'], width=width, label='EU Sales', color='firebrick')
    plt.bar([i + width for i in x], sales['JP Sales'], width=width, label='JP Sales', color='orange')
    plt.bar([i + 2 * width for i in x], sales['Other Sales'], width=width, label='Other Sales', color='gold')

    plt.xticks(x, publishers, rotation=45, ha='right')
    plt.xlabel('Publisher')
    plt.ylabel('Sales (in millions)')
    plt.title('Top 10 Publishers by Sales')
    plt.legend()
    plt.tight_layout()

    plt.savefig('static/charts/sales_by_publisher.png')
    plt.close()


def get_sales_by_genre_barchart():
    sales = data.groupby('Genre')[['NA Sales', 'EU Sales', 'JP Sales', 'Other Sales', 'Global Sales']].sum()
    sales = sales.round(2)
    sales = sales.sort_values(by='Global Sales', ascending=False)

    genres = sales.index.tolist()
    x = range(len(genres))

    width = 0.15
    plt.figure(figsize=(10, 6))

    plt.bar([i - 2 * width for i in x], sales['Global Sales'], width=width, label='Global Sales', color='silver')
    plt.bar([i - width for i in x], sales['NA Sales'], width=width, label='NA Sales', color='darkblue')
    plt.bar(x, sales['EU Sales'], width=width, label='EU Sales', color='firebrick')
    plt.bar([i + width for i in x], sales['JP Sales'], width=width, label='JP Sales', color='orange')
    plt.bar([i + 2 * width for i in x], sales['Other Sales'], width=width, label='Other Sales', color='gold')

    plt.xticks(x, genres, rotation=45, ha='right')
    plt.xlabel('Genre')
    plt.ylabel('Sales (in millions)')
    plt.title('Genres by Sales')
    plt.legend()
    plt.tight_layout()

    plt.savefig('static/charts/sales_by_genre.png')
    plt.close()


def na_sales_by_genre_over_time_top7_barchart():
    total_sales = data.groupby('Genre')['NA Sales'].sum().sort_values(ascending=False)
    top_genres = total_sales.head(7).index.tolist()

    filtered_data = data[data['Genre'].isin(top_genres)]
    sales = filtered_data.groupby(['Year', 'Genre'])['NA Sales'].sum().unstack().fillna(0)
    sales = sales.round(2)

    colors = ['darkblue', 'firebrick', 'orange', 'darkgreen', 'purple', 'teal', 'gold']

    plt.figure(figsize=(12, 7))
    for genre, color in zip(sales.columns, colors):
        plt.plot(sales.index, sales[genre], label=genre, color=color)

    plt.xlabel('Year')
    plt.ylabel('NA Sales (millions)')
    plt.title('North America Sales by Top 7 Genres Over Time')
    plt.legend(loc='upper right', fontsize='small')
    plt.tight_layout()

    plt.savefig('static/charts/na_sales_by_genre_top7.png')
    plt.close()
