import os
import base64
import pandas as pd
import numpy as np
from tpot_profit_classifier import predict_profit
from movieapp import construct_x, valid_inputs
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

# Load data on actors, directors and writers
actors_df = pd.read_csv("actors.csv")
directors_df = pd.read_csv("directors.csv")
writers_df = pd.read_csv("writers.csv")

# Genres, actors, directors, writers months.
genres = np.unique(np.hstack(DATAFRAME["Genre"]))
genres = genres[genres != None]
actors = actors_df["primaryName"].sort_values().values
directors = directors_df["primaryName"].sort_values().values
writers = writers_df["primaryName"].sort_values().values
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]



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
    columns = [item for item in columns if item not in
               ["Title", "Genre", "Director", "Actors", "Writer", "Plot", "Language", "Rated",
                "Country", "Awards", "tconst", "nconst", "Year"]]



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


    # Get the user inputs for prediction
    budget_predict = request.args.get("budget")
    runtime_predict = request.args.get("runtime")
    genre_predict = []
    for genre in genres:
        genre_predict.append(request.args.get(genre))
    actors_predict = request.args.get("actors")
    director_predict = request.args.get("director")
    writers_predict = request.args.get("writers")
    month_predict = request.args.get("month")

    # Check that all values are present before making a prediction
    prediction = ""
    if valid_inputs(runtime_predict,
                    budget_predict,
                    actors_predict,
                    director_predict,
                    writers_predict,
                    genre_predict,
                    month_predict,
                    actors_df,
                    directors_df,
                    writers_df
                    ):

        try:
            # Construct X from user inputs
            features = construct_x(
                                    runtime=runtime_predict,
                                    budget=budget_predict,
                                    actors=actors_predict,
                                    director=director_predict,
                                    writers=writers_predict,
                                    selected_genres=genre_predict,
                                    month=month_predict,
                                    actors_df=actors_df,
                                    directors_df=directors_df,
                                    writers_df=writers_df,
                                    genres=genres,
                                    months=months
                                    )
            
            prediction = predict_profit(features)

            if prediction == 1:
                prediction = "This movie should make you some profit!"
            else:
                prediction = "You'll likely lose your money with this movie."

        except:
            prediction = "Something went wrong with pipeline."

    else:
        prediction = """Check names and make sure they are exact matches from the list of actors, directors and writers.
                        Separate names with comma.
                        Rember to select release month and genres."""


    # Render the page
    return render_template("index.html",
                            plots=plots,
                            data=data,
                            columns=columns,
                            x_axis=x_axis,
                            y_axis=y_axis,
                            genres=genres,
                            directors=directors,
                            writers=writers,
                            actors=actors,
                            months = months,
                            saved_budget=budget_predict,
                            saved_runtime = runtime_predict,
                            saved_genres=genre_predict,
                            saved_actors=actors_predict,
                            saved_directors=director_predict,
                            saved_writers=writers_predict,
                            prediction=prediction
                            )

if __name__ == "__main__": 
    app.run(debug=False) 
