def decide_action(probability, retry_count, failure_type):

    retryable_failures = [
        "temporary",
        "network"
    ]

    # Safety rule: don't retry more than twice
    if retry_count >= 2:
        return "STOP"

    # High recovery probability + retryable failure
    if probability >= 0.80 and failure_type in retryable_failures:
        return "RETRY"

    # Medium probability
    if probability >= 0.50:
        return "NOTIFY CUSTOMER"

    # Low probability
    return "STOP"


# Test the decision engine
probability = 0.90
retry_count = 0
failure_type = "temporary"

action = decide_action(
    probability,
    retry_count,
    failure_type
)

print("Recovery Probability:", probability * 100, "%")
print("Recommended Action:", action)