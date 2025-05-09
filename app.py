import pandas as pd
from flask import Flask, render_template, request, jsonify

from analysis.analysis import *
from analysis.eda import *
from analysis.summary import (get_shape, get_info, get_head, get_describe, get_unique_counts)
from analysis.models import *
from analysis.chart_generation import *

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/summary')
def summary():
    unique_counts = get_unique_counts()
    shape_data = get_shape()
    describe_data = get_describe()
    return render_template('summary.html',
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


@app.route('/eda')
def eda():
    sales_data, total_row = sales_by_year()
    publishers_data = na_sales_by_top_publishers_action_games()
    action_publisher_data = na_sales_by_top_20_action_games()
    top_20_action_games = na_sales_by_top_20_action_games()
    na_by_genre = na_sales_by_genre()

    get_sales_by_year_linechart()
    get_sales_by_publisher_barchart()
    get_sales_by_genre_barchart()
    na_sales_by_genre_over_time_top7_barchart()

    return render_template('eda.html',
                           sales_data=sales_data,
                           total_row=total_row,
                           publishers_data=publishers_data,
                           action_publisher_data=action_publisher_data,
                           top_20_action_games=top_20_action_games,
                           na_by_genre=na_by_genre)


@app.route('/analysis')
def analysis():
    genres_2006_2011, publishers_2006_2011, platforms_2006_2011 = get_sales_data_for_period(2006, 2011)
    genres_2012_2016, publishers_2012_2016, platforms_2012_2016 = get_sales_data_for_period(2012, 2016)
    top_combinations_2006_2011 = top_na_sales_combinations(2006, 2011)
    top_combinations_2012_2016 = top_na_sales_combinations(2012, 2016)

    return render_template(
        'analysis.html',
        genres_2006_2011=genres_2006_2011,
        genres_2012_2016=genres_2012_2016,
        publishers_2006_2011=publishers_2006_2011,
        publishers_2012_2016=publishers_2012_2016,
        platforms_2006_2011=platforms_2006_2011,
        platforms_2012_2016=platforms_2012_2016,
        top_combinations_2006_2011=top_combinations_2006_2011,
        top_combinations_2012_2016=top_combinations_2012_2016,
    )


@app.route('/get_publishers/<genre>')
def get_publishers(genre):
    filtered_data = data[(data['Year'] >= 2012) & (data['Year'] <= 2016) & (data['Genre'] == genre)]
    publishers = sorted(filtered_data['Publisher'].dropna().unique())
    return jsonify(publishers)


@app.route('/get_platforms/<genre>/<publisher>')
def get_platforms(genre, publisher):
    filtered_data = data[(data['Year'] >= 2012) & (data['Year'] <= 2016) &
                         (data['Genre'] == genre) &
                         (data['Publisher'] == publisher)]
    platforms = sorted(filtered_data['Platform'].dropna().unique())
    return jsonify(platforms)


@app.route('/models', methods=['GET', 'POST'])
def models():
    model_2006_2011, encoders_2006_2011, metrics_2006_2011 = prepare_classification_data(2006, 2011)
    model_2012_2016, encoders_2012_2016, metrics_2012_2016 = prepare_classification_data(2012, 2016)

    combined_2006_2011 = zip(['Genre', 'Publisher', 'Platform'],
                            [round(val, 2) for val in model_2006_2011.feature_importances_])
    combined_2012_2016 = zip(['Genre', 'Publisher', 'Platform'],
                            [round(val, 2) for val in model_2012_2016.feature_importances_])

    # Get data for 2012-2016 period
    period_data = data[(data['Year'] >= 2012) & (data['Year'] <= 2016)]
    
    # Get unique genres
    genres = sorted(period_data['Genre'].dropna().unique())
    
    # Create dictionary of publishers for each genre
    publishers_by_genre = {}
    for genre in genres:
        publishers_by_genre[genre] = sorted(period_data[period_data['Genre'] == genre]['Publisher'].dropna().unique())
    
    # Create dictionary of platforms for each genre-publisher combination
    platforms_by_genre_publisher = {}
    for genre in genres:
        platforms_by_genre_publisher[genre] = {}
        for publisher in publishers_by_genre[genre]:
            platforms_by_genre_publisher[genre][publisher] = sorted(
                period_data[(period_data['Genre'] == genre) & 
                          (period_data['Publisher'] == publisher)]['Platform'].dropna().unique()
            )

    prediction_result = None
    if request.method == 'POST':
        genre = request.form['genre']
        publisher = request.form['publisher']
        platform = request.form['platform']
        
        prediction = get_prediction(model_2012_2016, encoders_2012_2016, genre, publisher, platform)
        prediction_result = 'Yes' if prediction == 1 else 'No'

    return render_template(
        'models.html',
        combined_2006_2011=combined_2006_2011,
        combined_2012_2016=combined_2012_2016,
        classifier_2006_2011=metrics_2006_2011,
        classifier_2012_2016=metrics_2012_2016,
        genres=genres,
        publishers_by_genre=publishers_by_genre,
        platforms_by_genre_publisher=platforms_by_genre_publisher,
        prediction_result=prediction_result
    )


if __name__ == '__main__':
    app.run(debug=True)
