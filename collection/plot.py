import pandas as pd
import matplotlib.pyplot as plt

def plot(year, month, day, timestamp):
    filename = "enf_data/" + str(year) + "/" + str(month) + "/" + str(day) + ".csv"
    df = pd.read_csv(filename)
    df = df[df["time"].str.contains(timestamp)]

    fig, ax = plt.subplots()
    ax.plot(df["time"], df["frequency"])
    fig.show()

plot(2024, 8, 19, "19.08.2024 00:")