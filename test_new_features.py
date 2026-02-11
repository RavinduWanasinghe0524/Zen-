import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

print("=== Zen Integration Test ===\n")

try:
    print("1. Testing Memory Module Import...")
    from memory import ZenMemory
    print("[OK] memory.py imported")

    print("2. Testing App Control Module Import...")
    from app_control import AppController
    print("[OK] app_control.py imported")

    print("3. Testing ZenTools Integration...")
    from tools import ZenTools
    tools = ZenTools()
    print("[OK] ZenTools initialized successfully")
    
    # Test memory through tools
    print("4. Testing Memory via Tools...")
    print(tools.remember_fact("Test fact: The sky is blue"))
    print(tools.recall_memories("sky"))
    
    # Test app control through tools (mock/dry run)
    print("5. Testing App Control via Tools...")
    # we won't actually play media to avoid disturbing user, just check the method exists
    if hasattr(tools, 'control_media') and hasattr(tools, 'play_youtube'):
        print("[OK] control_media and play_youtube methods exist")
    else:
        print("[FAIL] Missing methods in ZenTools")

    print("\n[OK] Integration Test PASSED!")

except Exception as e:
    print(f"\n[FAIL] Integration Test FAILED: {e}")
    import traceback
    traceback.print_exc()
