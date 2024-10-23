import random
import unittest

# --- Code for AppFeatures and AppDetector ---

class AppFeatures:
    """Class to represent the features of an online social network application."""
    def __init__(self, permissions, user_interactions, app_reviews):
        self.permissions = permissions
        self.user_interactions = user_interactions
        self.app_reviews = app_reviews

    def __str__(self):
        return (f"Permissions: {self.permissions}, "
                f"User Interactions: {self.user_interactions}, "
                f"App Reviews: {self.app_reviews}")

class AppDetector:
    """Class to detect if an app is good, neutral, or evil based on rules, with reasoning."""
    def __init__(self, threshold_permissions=5, min_reviews=100, neutral_review_threshold=200):
        self.threshold_permissions = threshold_permissions
        self.min_reviews = min_reviews
        self.neutral_review_threshold = neutral_review_threshold  # Threshold for marking as neutral

    def classify_app(self, app_features: AppFeatures):
        """Classifies the app as Good, Neutral, or Evil with reasoning."""
        reasons = []
        result = "Good"

        # Check for permissions issues
        if app_features.permissions > self.threshold_permissions + 2:
            reasons.append(f"Too many permissions requested (> {self.threshold_permissions + 2})")
            result = "Evil"
        elif app_features.permissions > self.threshold_permissions:
            reasons.append(f"Moderately high permissions (> {self.threshold_permissions})")
            if result != "Evil":
                result = "Neutral"

        # Check for review count
        if app_features.app_reviews < self.min_reviews:
            reasons.append(f"Too few reviews (< {self.min_reviews})")
            result = "Evil"
        elif app_features.app_reviews < self.neutral_review_threshold:
            reasons.append(f"Moderately low reviews (< {self.neutral_review_threshold})")
            if result != "Evil":
                result = "Neutral"

        # Check for user interaction
        if app_features.user_interactions < 5:
            reasons.append("Very low user interactions (< 5)")
            result = "Evil"
        elif app_features.user_interactions < 10:
            reasons.append("Low user interactions (< 10)")
            if result != "Evil":
                result = "Neutral"

        # If no reasons found and result is still Good, mark it as all criteria met
        if result == "Good":
            reasons.append("All criteria met")

        return result, reasons

# --- Unit Testing ---

class TestAppDetector(unittest.TestCase):
    """Unit tests for AppDetector."""
    
    def setUp(self):
        # Initialize AppDetector with thresholds for permissions, reviews, and neutral range
        self.detector = AppDetector(threshold_permissions=5, min_reviews=100, neutral_review_threshold=200)
    
    def test_evil_app_due_to_permissions(self):
        # Case where permissions far exceed the threshold
        app = AppFeatures(permissions=8, user_interactions=20, app_reviews=250)
        result, reasons = self.detector.classify_app(app)
        self.assertEqual(result, "Evil", "App should be classified as evil due to excessive permissions")
        print(f"\nTest: {app}\nResult: {result}\nReasons: {reasons}")
    
    def test_evil_app_due_to_low_reviews(self):
        # Case where reviews are far below the minimum threshold
        app = AppFeatures(permissions=4, user_interactions=20, app_reviews=50)
        result, reasons = self.detector.classify_app(app)
        self.assertEqual(result, "Evil", "App should be classified as evil due to low reviews")
        print(f"\nTest: {app}\nResult: {result}\nReasons: {reasons}")
    
    def test_neutral_app_due_to_permissions(self):
        # Test a neutral app with slightly high permissions but safe reviews and interactions
        app = AppFeatures(permissions=6, user_interactions=15, app_reviews=300)
        result, reasons = self.detector.classify_app(app)
        self.assertEqual(result, "Neutral", "App should be classified as neutral due to moderately high permissions")
        print(f"\nTest: {app}\nResult: {result}\nReasons: {reasons}")

    def test_good_app(self):
        # Test a good app with low permissions, good interactions, and high reviews
        app = AppFeatures(permissions=3, user_interactions=30, app_reviews=250)
        result, reasons = self.detector.classify_app(app)
        self.assertEqual(result, "Good", "App should be classified as good")
        print(f"\nTest: {app}\nResult: {result}\nReasons: {reasons}")

# --- Black-Box Testing ---

def black_box_test():
    """Perform black-box testing by running tests on various inputs without knowing internal logic."""
    detector = AppDetector()

    # Test apps with different feature combinations
    test_cases = [
        AppFeatures(permissions=9, user_interactions=25, app_reviews=100),   # Evil due to too many permissions
        AppFeatures(permissions=5, user_interactions=15, app_reviews=150),   # Neutral due to low reviews
        AppFeatures(permissions=4, user_interactions=30, app_reviews=400),   # Good app
        AppFeatures(permissions=5, user_interactions=9, app_reviews=250),    # Neutral due to low user interaction
    ]

    for i, app in enumerate(test_cases):
        result, reasons = detector.classify_app(app)
        print(f"\nBlack-Box Test Case {i+1}:\nApp Info: {app}\nResult: {result}\nReasons: {reasons}")

# --- White-Box Testing ---

def white_box_test():
    """Perform white-box testing by explicitly testing paths based on internal logic."""
    detector = AppDetector()

    # Case 1: Permissions too high
    app1 = AppFeatures(permissions=10, user_interactions=50, app_reviews=500)
    result, reasons = detector.classify_app(app1)
    assert result == "Evil", "App with too many permissions should be classified as evil"
    print(f"\nWhite-Box Case 1: {app1}\nResult: {result}\nReasons: {reasons}")

    # Case 2: Low reviews
    app2 = AppFeatures(permissions=4, user_interactions=30, app_reviews=80)
    result, reasons = detector.classify_app(app2)
    assert result == "Evil", "App with low reviews should be classified as evil"
    print(f"\nWhite-Box Case 2: {app2}\nResult: {result}\nReasons: {reasons}")

    # Case 3: Neutral app due to permissions
    app3 = AppFeatures(permissions=6, user_interactions=20, app_reviews=300)
    result, reasons = detector.classify_app(app3)
    assert result == "Neutral", "App with moderately high permissions should be neutral"
    print(f"\nWhite-Box Case 3: {app3}\nResult: {result}\nReasons: {reasons}")

    # Case 4: Good app
    app4 = AppFeatures(permissions=3, user_interactions=30, app_reviews=250)
    result, reasons = detector.classify_app(app4)
    assert result == "Good", "App with good stats should be classified as good"
    print(f"\nWhite-Box Case 4: {app4}\nResult: {result}\nReasons: {reasons}")

# --- Simulating Apps for Dynamic Testing ---

def simulate_app():
    """Function to simulate apps with random features."""
    return AppFeatures(
        permissions=random.randint(1, 10),
        user_interactions=random.randint(0, 50),
        app_reviews=random.randint(50, 500)
    )

# --- Main Function to Run All Tests ---

if __name__ == "__main__":
    # Run Unit Tests
    unittest.main(exit=False)  # Avoid exiting the program after running unit tests

    # Run Black-Box Testing
    print("\nRunning Black-Box Testing:")
    black_box_test()

    # Run White-Box Testing
    print("\nRunning White-Box Testing:")
    white_box_test()
