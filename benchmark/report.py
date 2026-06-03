import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from benchmark.tracker import get_sessions, get_stats


def print_full_report():
    sessions = get_sessions()

    if not sessions:
        print("No sessions logged yet.")
        return

    total = len(sessions)
    print("\n" + "=" * 65)
    print(" DEBUG AGENT - BENCHMARK REPORT")
    print("=" * 65)
    print(f" Total sessions logged: {total}")
    print("=" * 65)

    stats = get_stats()
    print("\n OVERALL STATS")
    print("-" * 65)
    print(f"  Autonomy Rate:        {stats['autonomy_rate']}%")
    print(f"  Acceptance Rate:      {stats['acceptance_rate']}%")
    print(f"  Avg Confidence:       {stats['avg_confidence']}")
    print(f"  Heavy Interventions:  {stats['heavy_rate']}%")
    print(f"  Medium Interventions: {stats['medium_rate']}%")

    print("\n IMPROVEMENT OVER ROUNDS (same 10 bugs repeated)")
    print("-" * 65)
    print(f"  {'Round':<18} {'Sessions':<10} {'Autonomy%':<12} "
          f"{'Accept%':<12} {'AvgConf':<10} {'Heavy%':<10}")
    print(f"  {'-'*16:<18} {'-'*7:<10} {'-'*9:<12} "
          f"{'-'*7:<12} {'-'*7:<10} {'-'*6:<10}")

    rounds = [
        ("Round 1 (1-10)", lambda s: s["session_id"] <= 10),
        ("Round 2 (11-20)", lambda s: 11 <= s["session_id"] <= 20),
        ("Round 3 (21-30)", lambda s: 21 <= s["session_id"] <= 30),
        ("Round 4 (31-40)", lambda s: 31 <= s["session_id"] <= 40),
    ]

    for round_name, round_filter in rounds:
        round_sessions = [s for s in sessions if round_filter(s)]
        if not round_sessions:
            continue

        n = len(round_sessions)
        autonomy = sum(1 for s in round_sessions if s["path"] == "autonomous")
        accepted = sum(1 for s in round_sessions if s["fix_accepted"])
        heavy = sum(1 for s in round_sessions if s["intervention_depth"] == "heavy")
        avg_conf = sum(s["avg_confidence"] for s in round_sessions) / n

        print(f"  {round_name:<18} {n:<10} "
              f"{autonomy/n*100:.0f}%{'':9}"
              f"{accepted/n*100:.0f}%{'':9}"
              f"{avg_conf:.3f}{'':5}"
              f"{heavy/n*100:.0f}%")

    print("\n IMPROVEMENT DELTA (round over round)")
    print("-" * 65)

    round_data = []
    for round_name, round_filter in rounds:
        round_sessions = [s for s in sessions if round_filter(s)]
        if not round_sessions:
            continue
        n        = len(round_sessions)
        autonomy = sum(1 for s in round_sessions if s["path"] == "autonomous")
        accepted = sum(1 for s in round_sessions if s["fix_accepted"])
        avg_conf = sum(s["avg_confidence"] for s in round_sessions) / n
        round_data.append({
            "name":     round_name,
            "autonomy": autonomy / n * 100,
            "accepted": accepted / n * 100,
            "avg_conf": avg_conf
        })

    if len(round_data) >= 2:
        for i in range(1, len(round_data)):
            prev = round_data[i - 1]
            curr = round_data[i]
            auto_delta = curr["autonomy"] - prev["autonomy"]
            acc_delta  = curr["accepted"] - prev["accepted"]
            conf_delta = curr["avg_conf"] - prev["avg_conf"]

            auto_arrow = "↑" if auto_delta > 0 else "↓" if auto_delta < 0 else "→"
            acc_arrow  = "↑" if acc_delta > 0 else "↓" if acc_delta < 0 else "→"
            conf_arrow = "↑" if conf_delta > 0 else "↓" if conf_delta < 0 else "→"

            print(f"  {prev['name']} → {curr['name']}")
            print(f"    Autonomy:    {auto_arrow} {auto_delta:+.1f}%")
            print(f"    Acceptance:  {acc_arrow} {acc_delta:+.1f}%")
            print(f"    Confidence:  {conf_arrow} {conf_delta:+.3f}")
            print()
    else:
        print("  Complete at least 2 rounds to see delta.")

    print("\n PER BUG TYPE BREAKDOWN")
    print("-" * 65)
    print(f"  {'Bug Type':<22} {'Sessions':<10} {'Autonomy%':<12} {'Accept%':<10}")
    print(f"  {'-'*20:<22} {'-'*7:<10} {'-'*9:<12} {'-'*7:<10}")

    bug_types = sorted(set(s["bug_type"] for s in sessions))
    for bug_type in bug_types:
        type_sessions = [s for s in sessions if s["bug_type"] == bug_type]
        n        = len(type_sessions)
        autonomy = sum(1 for s in type_sessions if s["path"] == "autonomous")
        accepted = sum(1 for s in type_sessions if s["fix_accepted"])
        print(f"  {bug_type:<22} {n:<10} "
              f"{autonomy/n*100:.0f}%{'':9}"
              f"{accepted/n*100:.0f}%")

    print("\n SESSION LOG")
    print("-" * 65)
    print(f"  {'ID':<5} {'Bug ID':<15} {'Type':<22} {'Path':<12} "
          f"{'Action':<8} {'Conf':<7} {'Depth':<10}")
    print(f"  {'-'*3:<5} {'-'*10:<15} {'-'*20:<22} {'-'*6:<12} "
          f"{'-'*6:<8} {'-'*4:<7} {'-'*8:<10}")

    for s in sessions:
        print(f"  {s['session_id']:<5} "
              f"{s['bug_id']:<15} "
              f"{s['bug_type']:<22} "
              f"{s['path']:<12} "
              f"{s['engineer_action']:<8} "
              f"{s['avg_confidence']:<7} "
              f"{s['intervention_depth']:<10}")

    print("\n" + "=" * 65)

if __name__ == "__main__":
    print_full_report()