import matplotlib.pyplot as plt
from pandas.plotting import table
from data.load_data import load_data

data = load_data()


def top7_na_sales_by_group(df, group_field):
    return (
        df.groupby(group_field, as_index=False)['NA Sales']
        .sum()
        .sort_values(by='NA Sales', ascending=False)
        .head(7)
        .round(2)
    )


def get_sales_data_for_period(start_year, end_year):
    df = data[(data['Year'] >= start_year) & (data['Year'] <= end_year)]
    genres = top7_na_sales_by_group(df, 'Genre')
    publishers = top7_na_sales_by_group(df, 'Publisher')
    platforms = top7_na_sales_by_group(df, 'Platform')
    return genres.to_dict(orient='records'), publishers.to_dict(orient='records'), platforms.to_dict(orient='records')


def save_sales_summary_chart(start1, end1, start2, end2, filename='data/analysis.png'):
    df1 = data[(data['Year'] >= start1) & (data['Year'] <= end1)]
    df2 = data[(data['Year'] >= start2) & (data['Year'] <= end2)]

    group_fields = ['Genre', 'Publisher', 'Platform']

    fig, axes = plt.subplots(3, 2, figsize=(22, 14))
    fig.suptitle(f'NA Sales Comparison: {start1}-{end1} vs {start2}-{end2}', fontsize=22)

    for i, group in enumerate(group_fields):
        result1 = top7_na_sales_by_group(df1, group)
        result2 = top7_na_sales_by_group(df2, group)

        ax1 = axes[i][0]
        ax2 = axes[i][1]

        ax1.axis('off')
        ax2.axis('off')

        ax1.set_title(f'{group} {start1}-{end1}', fontsize=14)
        ax2.set_title(f'{group} {start2}-{end2}', fontsize=14)

        tbl1 = table(ax1, result1, loc='center', colWidths=[0.3] * len(result1.columns))
        tbl2 = table(ax2, result2, loc='center', colWidths=[0.3] * len(result2.columns))

        for tbl in [tbl1, tbl2]:
            tbl.auto_set_font_size(False)
            tbl.set_fontsize(12)
            tbl.scale(1.2, 1.2)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(filename, bbox_inches='tight', pad_inches=0.3)
    plt.close()


def top_na_sales_combinations(start_year, end_year, top_n=10):
    df_period = data[(data['Year'] >= start_year) & (data['Year'] <= end_year)]

    combinations = (
        df_period
        .groupby(['Genre', 'Publisher', 'Platform'], as_index=False)['NA Sales']
        .sum()
        .sort_values(by='NA Sales', ascending=False)
        .head(top_n)
        .round(2)
    )

    return combinations.to_dict(orient='records')
