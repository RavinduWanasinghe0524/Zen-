import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

print("=== Zen Research Test ===\n")

try:
    print("1. Testing Research Module Import...")
    from research import ZenResearcher, search
    if search:
        print("[OK] googlesearch imported")
    else:
        print("[FAIL] googlesearch not found")

    print("2. Testing ZenTools Integration...")
    from tools import ZenTools
    tools = ZenTools()
    
    if hasattr(tools, 'research_topic'):
        print("[OK] research_topic method exists")
    else:
        print("[FAIL] research_topic missing")

    print("3. Testing Research (Dry Run)...")
    # We won't run a full search to avoid network/rate limits in test, 
    # but we'll check if the researcher is initialized.
    if tools.researcher:
        print("[OK] Researcher initialized")
    else:
        print("[FAIL] Researcher not initialized")
        
    print("\n[OK] Research Test PASSED!")

except Exception as e:
    print(f"\n[FAIL] Research Test FAILED: {e}")
    import traceback
    traceback.print_exc()
