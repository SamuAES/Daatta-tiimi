import json
import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

def merge_json_files(json_data_list, output_file):
    merged_data = []

    for json_data in json_data_list:
        try:
            data = json.loads(json_data)
            merged_data.append(data)
        except:
            continue

    # Check if the file exists already to choose whether to overwrite or to append
    if not os.path.isfile(output_file):
        with open(output_file, 'w') as outfile:
            outfile.write(json.dump(merged_data, outfile))
    else:
        with open(output_file) as outfile:
            file_data = json.load(outfile)

        file_data += merged_data
        with open(output_file, mode='w') as outfile:
            outfile.write(json.dumps(file_data))

if __name__ == "__main__":
    json_data_list = []

    imdb_df = pd.read_csv("imdb_codes.csv", header=0)

    start_index = 300
    end_index = len(imdb_df)

    for i in range(start_index, end_index):
        try:
            imdb_id = imdb_df["tconst"][i]
        except:
            break

        if pd.isnull(imdb_id):
            print(f"--skipping empty row {i}--")
            continue

        url = f"http://www.omdbapi.com/?i={imdb_id}&plot=full&apikey={API_KEY}"

        headers = {
            "accept": "application/json",
        }

        try:
            response = requests.get(url, headers=headers)
        except:
            break
        print(f"Adding Row: {i}, ID: {imdb_id}")
        json_data_list.append(response.text)

    output_file = "raw_movie_data.json"
    merge_json_files(json_data_list, output_file)
