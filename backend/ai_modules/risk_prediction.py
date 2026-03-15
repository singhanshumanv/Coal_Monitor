from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Training data

X = np.array([
    [5,0,0,0.0],
    [5,1,1,0.2],
    [10,3,2,0.3],
    [8,2,2,0.25],
    [4,0,1,0.0],
    [12,5,3,0.4],
    [6,0,0,0.0],
    [7,3,1,0.42]
])

y = [
    "LOW",
    "MEDIUM",
    "HIGH",
    "HIGH",
    "LOW",
    "HIGH",
    "LOW",
    "HIGH"
]

model = RandomForestClassifier()
model.fit(X, y)


def predict_risk(total_tasks, overdue, due_soon):

    if total_tasks == 0:
        overdue_ratio = 0
    else:
        overdue_ratio = overdue / total_tasks

    features = np.array([[total_tasks, overdue, due_soon, overdue_ratio]])

    prediction = model.predict(features)

    return prediction[0]