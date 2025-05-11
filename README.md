# Video Game Sales Analyses

## Summary of the Dataset
[Open file](data/summary.txt)

## Analysis
### All Regions
![Sales by Year](static/charts/sales_by_year.png)  

![Sales by Publisher](static/charts/sales_by_publisher.png)  

![Sales by Genre](static/charts/sales_by_genre.png)  

### North America Sales

![North America Sales by Top 7 Genres Over Time](static/charts/na_sales_by_genre_top7.png)  

![North America Sales 2006–2011 vs 2012–2016](data/analysis.png)  

## Model Analysis

![Model Results](data/model_results.png)

#### Regression Analysis
- The regression model predicts global sales based on genre, publisher, and platform
- Feature importance analysis shows how each factor contributes to sales predictions

#### Classification Analysis
- The classification model predicts whether a game will be successful (above average sales)
- These metrics help evaluate the model's ability to identify successful games

## Data  
https://www.kaggle.com/code/upadorprofzs/eda-video-game-sales  

## Setup
Framework: Flask  

### IDE
PyCharm Professional 2025.1  

## Run Docker
if __name__ == "__main__":  
    app.run(host="0.0.0.0", port=5000, debug=False)  
docker build -t vg-sales-analysis .  
docker run -p 5000:5000 vg-sales-analysis  