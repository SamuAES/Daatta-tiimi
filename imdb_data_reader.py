import sys, argparse
import pandas as pd

if __name__ == "__main__":
    imdb_file = ''
    parser = argparse.ArgumentParser(description="Read the .tsv format IMDb data files")
    parser.add_argument("file")
    args = parser.parse_args()
    imdb_file = args.file
    try:
        imdb_df = pd.read_csv(imdb_file, sep='\t', header=0, low_memory=False)
    except Exception as e:
        print(e)
        sys.exit(2)
    print(f"Shape: {imdb_df.shape}\nSample:\n{imdb_df}")
