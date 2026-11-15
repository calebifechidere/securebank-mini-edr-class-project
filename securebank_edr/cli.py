"""Text menu and reproducible demonstration for SecureBank Mini EDR."""
from __future__ import annotations

import argparse
from pathlib import Path
from .core import MiniEDR


def display_events(edr: MiniEDR) -> None:
    with edr._lock:
        events = list(edr.events[-20:])
    print("\n-- RECENT FILE EVENTS --")
    if not events:
        print("No events yet. Initial files are treated as the baseline.")
    for ev in events:
        print(f"{ev['timestamp_utc']} | {ev['event_type']:<8} | {ev['file']} | {ev['event_id']}")


def display_alerts(edr: MiniEDR) -> None:
    with edr._lock:
        alerts = list(edr.alerts)
    print("\n-- INCIDENTS / ALERTS --")
    if not alerts:
        print("No alerts. A normal single-file change should not trigger an alert.")
    for item in alerts:
        print(f"{item['incident_id']} | {item['severity']} | {item['status']} | {item['rule_reason']}")


def detail(edr: MiniEDR, incident_id: str) -> None:
    item = edr.get_incident(incident_id)
    if not item:
        print("Incident not found.")
        return
    print(f"\nINCIDENT: {item['incident_id']}")
    for key in ("timestamp_utc", "title", "severity", "status", "rule_reason"):
        print(f"{key}: {item[key]}")
    print("Affected training files: " + ", ".join(item["affected_files"]))
    print("Supporting event IDs: " + ", ".join(item["supporting_event_ids"]))
    print("Actions:")
    if not item["actions"]:
        print("  None yet")
    for action in item["actions"]:
        print(f"  {action['timestamp_utc']} | {action['action']} | {action['analyst']}")


def interactive(edr: MiniEDR) -> None:
    edr.start()
    print("\nSecureBank Mini EDR — EDUCATIONAL TRAINING PROTOTYPE")
    print("Monitoring: " + str(edr.training))
    print("Scope: only local .txt files in this folder; no real containment.")
    try:
        while True:
            print("\n[1] Simulate normal activity (1 file)")
            print("[2] Simulate suspicious activity (5 files)")
            print("[3] View event timeline")
            print("[4] View alerts")
            print("[5] Investigate incident")
            print("[6] Acknowledge incident")
            print("[7] Simulate containment (status only)")
            print("[8] View summary and export incident report")
            print("[9] Exit")
            choice = input("Select [1-9]: ").strip()
            if choice == "1":
                pre = len(edr.alerts)
                edr.simulate_normal()
                print("One fictional sample updated. Additional alerts generated:", len(edr.alerts) - pre)
            elif choice == "2":
                pre = len(edr.alerts)
                edr.simulate_suspicious()
                print("Five fictional sample files updated. Additional alerts generated:", len(edr.alerts) - pre)
                if len(edr.alerts) == pre:
                    print("A prior burst may be inside the cooldown window; try again after 12 seconds.")
            elif choice == "3":
                display_events(edr)
            elif choice == "4":
                display_alerts(edr)
            elif choice == "5":
                detail(edr, input("Incident ID: ").strip())
            elif choice in ("6", "7"):
                incident_id = input("Incident ID: ").strip()
                response = "ACKNOWLEDGED" if choice == "6" else "CONTAINMENT_SIMULATED"
                try:
                    item = edr.respond(incident_id, response)
                    print("Recorded response:", item["status"])
                except (KeyError, ValueError) as exc:
                    print("Cannot record response:", exc)
            elif choice == "8":
                print("\nSUMMARY:", edr.summary())
                print("Incident report saved to:", edr.export_report())
            elif choice == "9":
                break
            else:
                print("Choose a number from 1 to 9.")
    except (EOFError, KeyboardInterrupt):
        print("\nClosing demo.")
    finally:
        edr.stop()


def quick_demo(edr: MiniEDR) -> None:
    """Run a safe self-contained demonstration (no GUI required)."""
    edr.initialize_baseline()
    initial = len(edr.alerts)
    edr.simulate_normal()
    after_normal = len(edr.alerts)
    edr.simulate_suspicious()
    after_suspicious = len(edr.alerts)
    print("SecureBank Mini EDR — QUICK DEMONSTRATION")
    print(f"Normal activity: 1 file modified; new alerts = {after_normal-initial}")
    print(f"Suspicious activity: 5 files modified; new alerts = {after_suspicious-after_normal}")
    display_events(edr)
    display_alerts(edr)
    report = edr.export_report()
    print("Report:", report)
    print("All activity is synthetic and confined to:", edr.training)


def main() -> None:
    parser = argparse.ArgumentParser(description="SecureBank mini EDR: safe folder-monitoring prototype")
    parser.add_argument("--workspace", type=Path, help="Optional workspace for training files and runtime output")
    parser.add_argument("--quick-demo", action="store_true", help="Run normal and suspicious simulated changes, then exit")
    parser.add_argument("--threshold", type=int, default=5, help="Distinct files required to trigger an alert (default: 5)")
    args = parser.parse_args()
    workspace = args.workspace if args.workspace else Path(__file__).resolve().parent.parent
    edr = MiniEDR(workspace, threshold=args.threshold)
    if args.quick_demo:
        quick_demo(edr)
    else:
        interactive(edr)


if __name__ == "__main__":
    main()
