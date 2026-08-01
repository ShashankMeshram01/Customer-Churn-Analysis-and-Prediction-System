import subprocess
import sys
import os

def run_step(step_name, script):
    print(f"\n{'='*50}")
    print(f"  ▶  {step_name}")
    print(f"{'='*50}")
    result = subprocess.run([sys.executable, script], check=True)
    print(f"  ✅  {step_name} — Done!")
    return result

def main():
    print("\n" + "🚀 " * 20)
    print("   CUSTOMER CHURN ANALYSIS PROJECT — FULL RUN")
    print("🚀 " * 20)

    # ── Step 1: Database Connection (load data)
    run_step("Step 1: Database Connection & Data Load", "sqldatabase_connection.py")

    # ── Step 2: EDA (Exploratory Data Analysis)
    run_step("Step 2: Exploratory Data Analysis (EDA)", "eda.py")

    # ── Step 3: Preprocessing
    run_step("Step 3: Data Preprocessing", "preprocessing.py")

    # ── Step 4: Model Training
    run_step("Step 4: Model Training", "model_training.py")

    # ── Step 5: Model Evaluation
    run_step("Step 5: Model Evaluation", "model_evaluating.py")

    # ── Step 6: Visualization
    run_step("Step 6: Visualization (Charts)", "visualization.py")

    # ── Step 7: Launch Flask App
    print(f"\n{'='*50}")
    print(f"  ▶  Step 7: Launching Flask Web App")
    print(f"{'='*50}")
    print("\n  🌐  Open your browser at: http://127.0.0.1:5000")
    print("  🛑  Press CTRL+C to stop the server\n")
    subprocess.run([sys.executable, "churn_app.py"])

if __name__ == "__main__":
    main()