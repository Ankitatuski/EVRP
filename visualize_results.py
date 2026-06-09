import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("results.csv")

print(df.head())

# Cost comparison 

plt.figure()

plt.plot(
    df["Experiment"],
    df["MemeticEnergy"]+df["MemeticTime"],
    label="Memetic"
)

plt.plot(
    df["Experiment"],
    df["LeBaronEnergy"]+df["LeBaronTime"],
    label="LeBaron"
)

plt.xlabel("Experiment")
plt.ylabel("Cost")
plt.title("Cost Comparison")

plt.legend()

plt.show()

# Energy comparison
plt.figure()

plt.plot(
    df["Experiment"],
    df["MemeticEnergy"],
    label="Memetic"
)

plt.plot(
    df["Experiment"],
    df["LeBaronEnergy"],
    label="LeBaron"
)

plt.xlabel("Experiment")
plt.ylabel("Cost")
plt.title("Energy Comparison")

plt.legend()

plt.show()

# Time comparison
plt.figure()

plt.plot(
    df["Experiment"],
    df["MemeticTime"],
    label="Memetic"
)

plt.plot(
    df["Experiment"],
    df["LeBaronTime"],
    label="LeBaron"
)

plt.xlabel("Experiment")
plt.ylabel("Cost")
plt.title("Time Comparison")

plt.legend()

plt.show()

#___________________
# Winner frequency

winner_counts = df["Winner"].value_counts()

plt.figure()

winner_counts.plot(
    kind="bar"
)

plt.ylabel("Selections")

plt.title("AI Agent Decisions")

plt.show()
