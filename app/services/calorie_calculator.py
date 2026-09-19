class CalorieCalculator:
    """
    Executes standard, weight-based metabolic calorie tracking estimates
    utilizing task MET coefficients.
    """
    # Standard medical MET scores for our supported sport portfolio
    MET_VALUES = {
        "Running": 9.8,
        "Walking": 3.5,
        "Cycling": 7.5,
        "Skipping": 11.0,
        "Swimming": 8.0,
        "Jogging": 7.0,
        "Push-ups": 3.8,
        "Sit-ups": 3.8,
        "Squats": 5.0,
        "Planks": 2.8,
        "Stretching": 2.3,
        "Custom Routine": 6.0
    }

    @staticmethod
    def calculate(activity_type: str, duration_minutes: int, weight_kg: float) -> float:
        """
        Executes standard MET formula processing to output estimated calorie burns.
        """
        met = CalorieCalculator.MET_VALUES.get(activity_type, 5.0)
        # Standard Oxygen-Kcal consumption formula match
        calories = duration_minutes * (met * 3.5 * weight_kg / 200.0)
        return round(calories, 2)