from config import memory, CONFIDENCE_THRESHOLD, DEVELOPER_ID

def test_mem0_write():
    print("\n--- Testing Mem0 Write ---")
    result = memory.add(
        messages=[
            {"role": "user", "content": "I prefer early returns over nested conditionals"}
        ],
        user_id=DEVELOPER_ID
    )
    print("Write result:", result)
    return result

def test_mem0_search():
    print("\n--- Testing Mem0 Search ---")
    results = memory.search(
        query="error handling style preference",
        filters={"user_id": DEVELOPER_ID},
        limit=3
    )
    hits = results.get("results", [])
    print(f"Found {len(hits)} memories")
    for r in hits:
        print(f"  Score: {r['score']:.3f} | Memory: {r['memory']}")
    

def test_mem0_delete_all():
    print("\n--- Cleaning up test memories ---")
    memory.delete_all(user_id=DEVELOPER_ID)
    print("Test memories deleted")

if __name__ == "__main__":
    print("=== Testing all connections ===")
    
    # Test 1: write
    test_mem0_write()
    
    # Test 2: search
    test_mem0_search()
    
    # Test 3: cleanup
    test_mem0_delete_all()
    
    print("\n=== All tests passed ===")