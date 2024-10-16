import pandas as pd
import numpy as np



def is_valid_name(names, df):
    if all([name in df["primaryName"].values for name in names]):
        return True

def turn_into_list(names):
    return [name.strip() for name in names.split(",")]

def valid_inputs(runtime, budget, actors, director, writers, selected_genres, month, actors_df, directors_df, writers_df):
    if runtime is None:
        return False
    elif budget is None:
        return False
    elif not is_valid_name(turn_into_list(actors), actors_df):
        return False
    elif not is_valid_name(turn_into_list(director), directors_df):
        return False
    elif not is_valid_name(turn_into_list(writers), writers_df):
        return False
    elif all(item is None for item in selected_genres):
        return False
    elif month is None:
        return False
    else:
        return True

def construct_x(runtime, budget, actors, director, writers, selected_genres, month, actors_df, directors_df, writers_df, genres, months):
    """Construct vector of 1x47
    Args:
        runtime: Runtime of the film in minutes
        budget: The budget of the film in millions USD
        actors: A list of names of actors
        director: Name of director
        writers: A list of names of writers
        selected_genres: A list of genres of the film
        month: Release month
    Returns:
        Vector of shape 1x47. The vector is needed to predict
        wether a film with the selected features will make profit
        or not.
    """
    actors = turn_into_list(actors)
    director = turn_into_list(director)
    writers = turn_into_list(writers)


    # Select actors, director and writers
    actors_tmp = actors_df.loc[actors_df["primaryName"].isin(actors)]
    director_tmp = directors_df.loc[directors_df["primaryName"].isin(director)]
    writers_tmp = writers_df.loc[writers_df["primaryName"].isin(writers)]

    # create df for actors, director and writers
    averages_df = pd.DataFrame({"actors_avg_profits":[actors_tmp["avg_profit"].mean()],
                                "actors_avg_budgets":[actors_tmp["avg_budget"].mean()],
                                "actors_avg_nof_films":[actors_tmp["nof_films"].mean()],
                                "directors_avg_profits":[director_tmp["avg_profit"].mean()],
                                "directors_avg_budgets":[director_tmp["avg_budget"].mean()],
                                "directors_avg_nof_films":[director_tmp["nof_films"].mean()],
                                "writers_avg_profits":[writers_tmp["avg_profit"].mean()],
                                "writers_avg_budgets":[writers_tmp["avg_budget"].mean()],
                                "writers_avg_nof_films":[writers_tmp["nof_films"].mean()],
                                })
    
    # create df of genres
    genres_df = pd.DataFrame(np.zeros((1, len(selected_genres))), columns=genres)
    for genre in selected_genres:
        genres_df.loc[0, genre] = 1

    # create df of months
    months_df = pd.DataFrame(np.zeros((1,len(months))), columns=months) 
    months_df.loc[0, month] = 1

    # create X
    budget = int(budget)*1000000
    X = pd.DataFrame({"Runtime":[runtime], "adjusted_prod_budget":[budget]})
    X = pd.concat((X, averages_df, genres_df, months_df), axis=1)
    X.columns = X.columns.astype(str)
    X = X.drop(columns="None")
    
    return X
    