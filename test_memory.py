import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent.memory import retrieve_memories, extract_principle, save_memory, get_all_memories

print("=== Testing Memory Module ===")

# Test 1: save an accept memory
print("\n--- Test 1: Save accept memory ---")
save_memory(
    bug="Function returns None instead of empty list",
    bug_type="return_type",
    action="a",
    suggested_fix="return None if no results found"
)

# Test 2: save a reject memory
print("\n--- Test 2: Save reject memory ---")
save_memory(
    bug="Missing null check before accessing attribute",
    bug_type="null_check",
    action="r",
    suggested_fix="Use try/except to handle None",
    reason="Prefer explicit None checks over try/except"
)

# Test 3: save an edit memory with principle extraction
print("\n--- Test 3: Save edit memory with principle extraction ---")
principle = extract_principle(
    bug="Exception handling using bare except",
    suggested_fix="try:\n    result = process()\nexcept:\n    pass",
    edit="try:\n    result = process()\nexcept ValueError as e:\n    logger.error(e)\n    raise"
)
print(f"Extracted principle: {principle}")
save_memory(
    bug="Exception handling using bare except",
    bug_type="exception_handling",
    action="e",
    suggested_fix="try/except bare",
    edited="specific exception with logging",
    principle=principle
)

# Test 4: retrieve memories
print("\n--- Test 4: Retrieve memories ---")
memories = retrieve_memories(
    bug_description="function not handling None return value",
    bug_type="null_check"
)
print(f"Retrieved {len(memories)} memories")
for m in memories:
    print(f"  Score: {m['score']:.3f} | {m['memory']}")

# Test 5: get all memories
print("\n--- Test 5: All stored memories ---")
all_mems = get_all_memories()
print(f"Total memories stored: {len(all_mems)}")
for m in all_mems:
    print(f"  - {m['memory']}")