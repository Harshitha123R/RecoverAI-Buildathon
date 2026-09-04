import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


# 1. Load our dataset
df = pd.read_csv("../data/payments.csv")

print("Dataset loaded!")
print("Shape:", df.shape)


# 2. Separate features and target
X = df.drop("recovered", axis=1)
y = df["recovered"]


# 3. Tell Python which columns contain text
categorical_features = [
    "payment_method",
    "failure_type"
]


# 4. Preprocessing for text columns
preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        )
    ],
    remainder="passthrough"
)


# 5. Create our ML model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)


# 6. Combine preprocessing + model
pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", model)
])


# 7. Split data into training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# 8. Train the model
pipeline.fit(X_train, y_train)


# 9. Make predictions
y_pred = pipeline.predict(X_test)


# 10. Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, zero_division=0)
recall = recall_score(y_test, y_pred, zero_division=0)
f1 = f1_score(y_test, y_pred, zero_division=0)


print("\n===== RECOVERAI MODEL =====")
print(f"Accuracy : {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall   : {recall:.2f}")
print(f"F1 Score : {f1:.2f}")


# 11. Test with a new failed payment
new_payment = pd.DataFrame([{
    "amount": 2500,
    "previous_successes": 8,
    "previous_failures": 1,
    "retry_count": 0,
    "customer_age_days": 300,
    "payment_method": "UPI",
    "failure_type": "temporary",
    "hour": 14
}])


# 12. Calculate recovery probability
probability = pipeline.predict_proba(new_payment)[0][1]


print("\n===== NEW PAYMENT =====")
print(f"Recovery Probability: {probability * 100:.2f}%")


# 13. Decide what RecoverAI should do
if probability >= 0.80:
    action = "RETRY"
elif probability >= 0.50:
    action = "NOTIFY CUSTOMER"
else:
    action = "STOP"


print("Recommended Action:", action)