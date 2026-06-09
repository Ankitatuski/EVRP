from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, root_mean_squared_error
import csv
import numpy as np
import matplotlib.pyplot as plt
import joblib


def retrain(file = "ev_energy_dataset.csv"):
    data = []
    with open(file, newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                row = [float(x) for x in row]
            except:
                True
            data.append(row)
    del data[1]
    del data[1]
    data = np.astype(np.array(data[1:]),float)

    #print(data[0:5])

    x = data[1:,1:]
    y = data[1:,0]

    print(y[:5])

    # Split data
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=42
    )

    # Train linear regression
    model = LinearRegression()
    model.fit(x_train, y_train)
    joblib.dump(model, "model.pkl")

    return model, x_test, y_test, x, y

if __name__ =="__main__":

    model, x_test, y_test, x, y = retrain()
    # Predict continuous values
    y_pred_continuous = model.predict(x_test)

    # Convert to class labels
    y_pred = (y_pred_continuous >= 0.5).astype(int)

    print("Continuous predictions:", y_pred_continuous)
    #print("Class predictions:", y_pred_)

    mae = mean_absolute_error(y_test, y_pred_continuous)
    mse = root_mean_squared_error(y_test, y_pred_continuous)
    print("MAE:", mae, "\tmin:",min(y)," max:",max(y))
    print("RMSE:", mse)

    plt.scatter(y_test, y_pred_continuous, alpha=0.5)
    plt.plot(
        [min(y_test), max(y_test)],
        [min(y_test), max(y_test)],
        color='red'
    )
    plt.xlabel("Actual")
    plt.ylabel("Predicted")
    plt.title("Actual vs Predicted")
    plt.show()
