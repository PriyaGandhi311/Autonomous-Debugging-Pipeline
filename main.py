import os
import sys
import time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from agent.memory import retrieve_memories, extract_principle, save_memory
from agent.confidence import compute_confidence, should_act_autonomously, confidence_label
from agent.fixer import generate_fix
from agent.steering import autonomous_steer
from agent.reviewer import show_fix, get_feedback, show_session_summary
from benchmark.tracker import log_session, get_next_session_id


def load_bug_file(filepath: str) -> tuple:
    with open(filepath, "r") as f:
        lines = f.readlines()

    bug_type = "general"
    bug_description = "Bug found in code"

    for line in lines:
        if line.startswith("# Bug type:"):
            bug_type = line.replace("# Bug type:", "").strip()
        if line.startswith("# Description:"):
            bug_description = line.replace("# Description:", "").strip()

    code = "".join(lines)
    return code, bug_description, bug_type


def run_debug_session(code: str, bug_description: str,
                      bug_type: str, bug_id: str):
    session_id = get_next_session_id()
    print(f"\n{'='*60}")
    print(f" Session {session_id} | Bug: {bug_id} | Type: {bug_type}")
    print(f"{'='*60}")

    memories = retrieve_memories(bug_description, bug_type)
    confidence = compute_confidence(memories)
    conf_label = confidence_label(confidence)

    print(f" Memories retrieved: {len(memories)} | {conf_label}")

    steering = None

    if should_act_autonomously(confidence):
        path = "autonomous"
        print(" Routing to: AUTONOMOUS PATH")
        steering, fix = autonomous_steer(bug_description, code, memories)
    else:
        path = "human"
        print(" Routing to: HUMAN-IN-LOOP PATH")
        fix = generate_fix(code, bug_description, memories)

    show_fix(bug_description, fix, conf_label, path, steering)
    if path == "autonomous":
        action = "a"
        reason = None
        edited = None
        principle = None
        print("\n [AUTO] Fix applied autonomously. No intervention needed.")
    else:
        feedback = get_feedback()
        action   = feedback["action"]
        reason   = feedback.get("reason")
        edited   = feedback.get("edited")

        principle = None
        if action == "e" and edited:
            print("\n Extracting preference from your edit...")
            principle = extract_principle(bug_description, fix, edited)
            print(f" Principle learned: {principle}")

    save_memory(
        bug=bug_description,
        bug_type=bug_type,
        action=action,
        suggested_fix=fix,
        reason=reason,
        edited=edited,
        principle=principle
    )

    log_session(
        session_id=session_id,
        bug_id=bug_id,
        bug_type=bug_type,
        memories_retrieved=len(memories),
        avg_confidence=confidence,
        path=path,
        action=action,
        steering=steering
    )

    show_session_summary(session_id, path, action, confidence, len(memories))


def run_canonical_benchmark():
    canonical_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "benchmark", "canonical_bugs"
    )
    bug_files = sorted(f for f in os.listdir(canonical_dir)
                       if f.endswith(".py"))

    if not bug_files:
        print("No canonical bug files found in benchmark/canonical_bugs/")
        return

    print(f"\n Running canonical benchmark - {len(bug_files)} bugs")

    for bug_file in bug_files:
        filepath = os.path.join(canonical_dir, bug_file)
        code, bug_description, bug_type = load_bug_file(filepath)
        run_debug_session(
            code=code,
            bug_description=bug_description,
            bug_type=bug_type,
            bug_id=bug_file.replace(".py", "")
        )
        print(" Waiting 15 seconds before next session...")
        time.sleep(15) 
        


def run_single_bug(filepath: str):
    code, bug_description, bug_type = load_bug_file(filepath)
    bug_id = os.path.basename(filepath).replace(".py", "")
    run_debug_session(code, bug_description, bug_type, bug_id)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Debug Agent")
    parser.add_argument(
        "--mode",
        choices=["canonical", "single", "report"],
        default="canonical",
        help="canonical: run all benchmark bugs | single: run one bug file | report: show benchmark report"
    )
    parser.add_argument(
        "--file",
        type=str,
        help="Path to bug file (required for --mode single)"
    )
    args = parser.parse_args()

    if args.mode == "canonical":
        run_canonical_benchmark()

    elif args.mode == "single":
        if not args.file:
            print("Error: --file required for single mode")
            sys.exit(1)
        run_single_bug(args.file)

    elif args.mode == "report":
        from benchmark.report import print_full_report
        print_full_report()