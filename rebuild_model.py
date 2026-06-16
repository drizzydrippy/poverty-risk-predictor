
"""
Run this file if you get:
ModuleNotFoundError
ValueError during unpickling
sklearn version mismatch errors
"""

import joblib
import sklearn

print("Current sklearn version:", sklearn.__version__)

# IMPORTANT:
# Re-train your model in the SAME environment/version
# then save again.

# Example:
# joblib.dump(model, "poverty_trap_model.pkl")

print("Rebuild completed.")
