class RiskEngine:

    IMAGE_WEIGHT = 30
    BATCH_WEIGHT = 25
    EXPIRY_WEIGHT = 40
    ANOMALY_WEIGHT = 20  # for future use

    @staticmethod
    def calculate(image_score: float, batch_match: bool, expiry_valid: bool):
        risk_score = 0
        breakdown = {
            "image_authenticity": 0,
            "batch_validation": 0,
            "expiry_validation": 0
        }

        # Image authenticity
        if image_score < 0.7:
            breakdown["image_authenticity"] = RiskEngine.IMAGE_WEIGHT
            risk_score += RiskEngine.IMAGE_WEIGHT

        # Batch validation
        if not batch_match:
            breakdown["batch_validation"] = RiskEngine.BATCH_WEIGHT
            risk_score += RiskEngine.BATCH_WEIGHT

        # Expiry validation
        if not expiry_valid:
            breakdown["expiry_validation"] = RiskEngine.EXPIRY_WEIGHT
            risk_score += RiskEngine.EXPIRY_WEIGHT

        # Verdict logic
        if risk_score < 30:
            verdict = "Genuine"
        elif risk_score < 60:
            verdict = "Suspicious"
        else:
            verdict = "Likely Fake"

        return risk_score, verdict, breakdown