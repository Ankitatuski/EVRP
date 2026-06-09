import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("results.csv")

print(df.head())

# Cost comparison

plt.figure()

plt.plot(
    df["Experiment"],
    df["MemeticCost"],
    label="Memetic"
)

plt.plot(
    df["Experiment"],
    df["LeBaronCost"],
    label="LeBaron"
)

plt.xlabel("Experiment")
plt.ylabel("Cost")
plt.title("Cost Comparison")

plt.legend()

plt.show()


# Winner frequency

winner_counts = df["Winner"].value_counts()

plt.figure()

winner_counts.plot(
    kind="bar"
)

plt.ylabel("Selections")

plt.title("AI Agent Decisions")

plt.show()
