from flask import Flask, render_template

from analysis.analysis import *
from analysis.sales import *
from analysis.eda import (get_shape, get_info, get_head, get_describe, get_unique_counts)
from analysis.chart_generation import *

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/eda')
def eda():
    unique_counts = get_unique_counts()
    shape_data = get_shape()
    describe_data = get_describe()
    return render_template('eda.html',
                           unique_counts=unique_counts,
                           shape_data=shape_data,
                           describe_data=describe_data)


@app.route('/info')
def info():
    info_data = get_info()
    head_data = get_head()
    return render_template('info.html', info_data=info_data, head_data=head_data)


@app.route('/charts')
def graphs():
    get_name_histogram()
    get_platform_histogram()
    get_genre_histogram()
    get_publisher_histogram()
    return render_template('charts.html')


@app.route('/sales')
def sales():
    sales_data, total_row = sales_by_year()
    publishers_data = na_sales_by_top_publishers_action_games()
    action_publisher_data = na_sales_by_top_20_action_games()
    top_20_action_games = na_sales_by_top_20_action_games()
    na_by_genre = na_sales_by_genre()

    get_sales_by_year_linechart()
    get_sales_by_publisher_barchart()
    get_sales_by_genre_barchart()
    na_sales_by_genre_over_time_top7_barchart()

    return render_template('sales.html',
                           sales_data=sales_data,
                           total_row=total_row,
                           publishers_data=publishers_data,
                           action_publisher_data=action_publisher_data,
                           top_20_action_games=top_20_action_games,
                           na_by_genre=na_by_genre)

@app.route('/analysis')
def analysis():
    genres_2006_2011, publishers_2006_2011 = get_sales_data_for_period(2006, 2011)
    genres_2012_2016, publishers_2012_2016 = get_sales_data_for_period(2012, 2016)

    return render_template(
        'analysis.html',
        genres_2006_2011=genres_2006_2011,
        genres_2012_2016=genres_2012_2016,
        publishers_2006_2011=publishers_2006_2011,
        publishers_2012_2016=publishers_2012_2016,
    )


if __name__ == '__main__':
    app.run(debug=True)
