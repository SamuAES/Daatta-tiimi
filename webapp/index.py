import base64
import pandas as pd
from io import BytesIO
from flask import Flask, render_template, request
from matplotlib.figure import Figure

app = Flask(__name__)

# Change this to point to the data to be used for the web app
DATAFRAME = pd.read_pickle('../movie_data.pkl')
# Set the default axes
DEFAULT_X = "Production budget"
DEFAULT_Y = "profit"

@app.route("/", methods=["GET", "POST"])
def home():
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
    # Render the page with the data
    return render_template("index.html", data=data, columns=columns, x_axis=x_axis, y_axis=y_axis)

if __name__ == "__main__": 
    app.run(debug=False) 
