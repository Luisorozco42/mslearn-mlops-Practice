# Import libraries

import argparse
import glob
import os

import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import mlflow 


# define functions
def main(args):
    #It begins a new execution of MLflow
    mlflow.start_run()
    
    # read data
    df = get_csvs_df(args.training_data)

    # split data
    X_train, X_test, y_train, y_test = split_data(df)

    # train model
    train_model(args.reg_rate, X_train, X_test, y_train, y_test)
    
    mlflow.log_params({"reg_rate": args.reg_rate})
    mlflow.end_run()

def get_csvs_df(path):
    if not os.path.exists(path):
        raise RuntimeError(f"Cannot use non-existent path provided: {path}")
    csv_files = glob.glob(f"{path}/*.csv")
    if not csv_files:
        raise RuntimeError(f"No CSV files found in provided data path: {path}")
    return pd.concat((pd.read_csv(f) for f in csv_files), sort=False)


def split_data(df):
    
    X = df.drop(columns=['Diabetic'])  
    y = df['Diabetic'] 
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)  # Ajusta los parámetros según tus necesidades

    return X_train, X_test, y_train, y_test

def train_model(reg_rate, X_train, X_test, y_train, y_test):
    # train model
    model = LogisticRegression(C=1/reg_rate, solver="liblinear").fit(X_train, y_train)
    
    accuracy = model.score(X_test, y_test)
    print(f"Accuracy of the model in the test set: {accuracy}")

def parse_args():
    # setup arg parser
    parser = argparse.ArgumentParser()

    # add arguments
    parser.add_argument("--training_data", dest='training_data',
                        type=str)
    parser.add_argument("--reg_rate", dest='reg_rate',
                        type=float, default=0.01)

    # parse args
    args = parser.parse_args()

    # return args
    return args

# run script
if __name__ == "__main__":
    # add space in logs
    print("\n\n")
    print("*" * 60)

    with mlflow.start_run():
        # parse args
        args = parse_args()
        
        # run main function
        main(args)
    # add space in logs
    print("*" * 60)
    print("\n\n")
