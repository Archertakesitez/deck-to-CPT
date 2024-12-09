import pandas as pd
import os


def convert_csv_to_pickle():
    """Convert CSV to pickle format if pickle file doesn't exist"""
    csv_file = "../data/cpt_codes_cleaned.csv"
    pickle_file = "../data/cpt_codes.pkl"

    if not os.path.exists(pickle_file):
        print("Converting CSV to pickle format...")
        df = pd.read_csv(csv_file)
        df.to_pickle(pickle_file)
        print("Conversion complete!")
    else:
        print("Pickle file already exists!")


def load_cpt_data():
    """Load CPT data from pickle file"""
    pickle_file = "../data/cpt_codes.pkl"
    return pd.read_pickle(pickle_file)


if __name__ == "__main__":
    convert_csv_to_pickle()
