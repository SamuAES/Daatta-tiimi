import os
import base64
import pandas as pd
from datetime import datetime
from io import BytesIO
from flask import Flask, render_template, request
from matplotlib.figure import Figure

app = Flask(__name__)

# Change this to point to the data to be used for the web app
DATAFRAME = pd.read_pickle('../movie_data_with_budgets.pkl')
# Set the default axes
DEFAULT_X = "log_profit"
DEFAULT_Y = "adjusted_prod_budget"

def predict(budget: int, genres: list, directors: list, writers: list, actors: list,
    release_date: datetime):
    """Predict the profit and ratings based on the given data
    Args:
        budget: The budget of the film in USD
        genres: A list of genres for the film
        directors: A list of directors for the film
        writers: A list of writers for the film
        actors: A list of actors for the film
        release_date: A datetime object denoting the release date of the film
    Returns:
        A prediction dict of the following keys:
            profit (the predicted profit)
            imdb (the predicted IMDB rating)
            metascore (the predicted Metascore rating)
            rottentomatoes (the predicted RottenTomatoes rating)"""

    # Initialize the dict for the prediction results
    predictions = {
        "profit": 0.0,
        "imdb": 0.0,
        "metascore": 0,
        "rottentomatoes": 0
    }

    # Predict the values
    # TODO: Add the prediction model methods here and add the results to predictions

    return predictions

@app.route("/", methods=["GET", "POST"])
def home():
    # Get ready-made plots
    plots = os.listdir("static/plots")
    plots = ["plots/" + file for file in plots]
    # Get column params
    x_axis = request.args.get("x-axis")
    y_axis = request.args.get("y-axis")
    # Set to default if not found
    if not x_axis:
        x_axis = DEFAULT_X
    if not y_axis:
        y_axis = DEFAULT_Y
    # Get columns
    columns = list(DATAFRAME)
    # Create the figure
    fig = Figure()
    ax = fig.subplots()
    ax.scatter(DATAFRAME[x_axis], DATAFRAME[y_axis], color="blue", alpha=0.2)
    ax.set_title(f"{x_axis} in relation to {y_axis}")
    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    # Save the figure to a temporary buffer
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Encode the data into a format that can be rendered on the page
    data = base64.b64encode(buf.getbuffer()).decode("ascii")

    # Get the genres, directors, writers and actors
    # TODO: Get the actual values for the dataset
    genres = ["Genre 1", "Genre 2", "Genre 3", "Genre 4", "Genre 5"]
    directors = ["Alfa", "Bravo", "Charlie"]
    writers = ["Delta", "Echo", "Foxtrot"]
    actors = ["Golf", "Hotel", "India", "Juliett", "Kilo", "Lima"]
    # Get the data for the prediction model
    budget_predict = request.args.get("budget")
    genre_predict = request.args.getlist("genre")
    director_predict = request.args.getlist("director")
    writer_predict = request.args.getlist("writer")
    actor_predict = request.args.getlist("actor")
    release_date_str = request.args.get("release-date")
    try:
        release_predict = datetime.strptime(release_date_str, "%Y-%m-%d")
    except:
        release_predict = None
    # Check that all values are present before making a prediction, otherwise set everything to None
    if budget_predict and genre_predict and director_predict and writer_predict and actor_predict and release_predict: 
        predictions = predict(budget_predict, genre_predict, director_predict, writer_predict,
            actor_predict, release_predict)
    else:
        predictions = {
            "profit": None,
            "imdb": None,
            "metascore": None,
            "rottentomatoes": None
        }

    # Render the page
    return render_template("index.html", data=data, columns=columns, x_axis=x_axis, y_axis=y_axis,
        genres=genres, directors=directors, writers=writers, actors=actors,
        saved_budget=budget_predict, saved_genres=genre_predict, saved_directors=director_predict,
        saved_writers=writer_predict, saved_actors=actor_predict, saved_release=release_date_str,
        predicted_profit=predictions["profit"], predicted_imdb=predictions["imdb"],
        predicted_metascore=predictions["metascore"],
        predicted_rottentomatoes=predictions["rottentomatoes"], plots=plots)

if __name__ == "__main__": 
    app.run(debug=False) 
