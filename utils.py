import pandas as pd

def load_data():
    """Load or generate sample motor vehicle collision data"""

    df = pd.read_csv("data/Cleaned_Motor_Vehicle_Collisions_Crashes.csv")
    #df['date'] = pd.to_datetime(df['date'])

    print(df.head())
    return df