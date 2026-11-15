
def generate_mock_prediction(farm_id: str, file_name: str):
    """
    Generates a deterministic mock crop-risk prediction.
    This is dummy output, not a real ML model prediction.
    """

    risk_levels = ["Low", "Medium", "High"]

    # Generate a consistent result for the same farm
    index = sum(ord(char) for char in farm_id) % 3

    risk_class = risk_levels[index]

    scores = {
        "Low": 0.25,
        "Medium": 0.55,
        "High": 0.85
    }

    return {
        "farm_id": farm_id,
        "file_name": file_name,
        "risk_class": risk_class,
        "score": scores[risk_class],
        "prediction_type": "mock",
        "status": "success"
    }
