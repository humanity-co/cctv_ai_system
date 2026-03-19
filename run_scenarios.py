import os
import sys
from process_video import process_cctv_video

def main():
    scenarios = {
        "1": {"name": "Indian Traffic (General)", "file": "datasets/cctv_sample.mp4"},
        "2": {"name": "High Density Traffic & Pedestrians", "file": "datasets/scenarios/traffic.mp4"},
        "3": {"name": "Fire & Environmental Hazard Demo", "file": "datasets/scenarios/fire_demo.mp4"},
        "4": {"name": "Security: Abandoned Objects & Intrusions", "file": "datasets/scenarios/traffic.mp4"}, # Multi-purpose
    }

    print("\n" + "="*40)
    print("  AIGuard PRO - SCENARIO SELECTOR")
    print("="*40)
    for k, v in scenarios.items():
        print(f"[{k}] {v['name']}")
    print("="*40)

    choice = input("\nSelect a scenario to run AI Analysis (1-4): ")
    
    if choice in scenarios:
        scenario = scenarios[choice]
        print(f"\n🚀 Launching Scenario: {scenario['name']}...")
        process_cctv_video(scenario["file"])
    else:
        print("❌ Invalid choice. Exiting.")

if __name__ == "__main__":
    # Ensure PYTHONPATH is set
    sys.path.append(os.getcwd())
    main()
