import random
import pandas as pd

random.seed(42)

payment_methods = ["UPI", "Card", "NetBanking", "Wallet"]
failure_types = ["temporary", "declined", "expired", "network"]

rows = []

for _ in range(1000):
    amount = round(random.uniform(100, 10000), 2)
    previous_successes = random.randint(0, 20)
    previous_failures = random.randint(0, 5)
    retry_count = random.randint(0, 3)
    customer_age_days = random.randint(10, 1000)
    payment_method = random.choice(payment_methods)
    failure_type = random.choice(failure_types)
    hour = random.randint(0, 23)

    # Synthetic recovery logic
    score = 0

    if previous_successes >= 5:
        score += 2

    if retry_count <= 1:
        score += 2

    if failure_type == "temporary":
        score += 3

    if failure_type == "network":
        score += 2

    if previous_failures <= 1:
        score += 1

    if customer_age_days >= 180:
        score += 1

    probability = score / 9

    recovered = 1 if random.random() < probability else 0

    rows.append([
        amount,
        previous_successes,
        previous_failures,
        retry_count,
        customer_age_days,
        payment_method,
        failure_type,
        hour,
        recovered
    ])

columns = [
    "amount",
    "previous_successes",
    "previous_failures",
    "retry_count",
    "customer_age_days",
    "payment_method",
    "failure_type",
    "hour",
    "recovered"
]

df = pd.DataFrame(rows, columns=columns)

df.to_csv("../data/payments.csv", index=False)

print("Dataset created successfully!")
print(df.head())
print("\nShape:", df.shape)