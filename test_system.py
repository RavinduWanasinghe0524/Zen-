"""
Zen Voice Assistant - Comprehensive System Test
Tests all components and dependencies to ensure everything is working correctly.
"""

import sys
import os

def test_imports():
    """Test all required imports."""
    print("=" * 70)
    print("TESTING IMPORTS")
    print("=" * 70)
    
    tests = {
        "Core Speech": ["speech_recognition", "pyttsx3"],
        "AI Provider": ["google.generativeai"],
        "System Utils": ["psutil", "dotenv", "pyautogui"],
        "GUI": ["tkinter"],
        "Optional": ["requests", "json", "threading", "time"]
    }
    
    results = {}
    for category, modules in tests.items():
        print(f"\n{category}:")
        for module in modules:
            try:
                __import__(module)
                print(f"  [OK] {module}")
                results[module] = True
            except ImportError as e:
                print(f"  ✗ {module} - {e}")
                results[module] = False
    
    return results

def test_config():
    """Test configuration."""
    print("\n" + "=" * 70)
    print("TESTING CONFIGURATION")
    print("=" * 70)
    
    try:
        from config import Config
        print(f"\n✓ Config loaded successfully")
        print(f"  • AI Provider: {Config.AI_PROVIDER}")
        print(f"  • GUI Enabled: {Config.GUI_ENABLED}")
        print(f"  • GUI Mode: {Config.GUI_MODE}")
        print(f"  • Wake Word Enabled: {Config.WAKE_WORD_ENABLED}")
        print(f"  • Speech Rate: {Config.SPEECH_RATE} WPM")
        
        errors = Config.validate_config()
        if errors:
            print("\n✗ Configuration errors:")
            for error in errors:
                print(f"  - {error}")
            return False
        else:
            print("\n✓ Configuration is valid!")
            return True
    except Exception as e:
        print(f"\n✗ Config test failed: {e}")
        return False

def test_modules():
    """Test main modules."""
    print("\n" + "=" * 70)
    print("TESTING MAIN MODULES")
    print("=" * 70)
    
    modules = [
        "listen",
        "speak", 
        "brain",
        "tools",
        "config",
        "logger",
        "daily_tasks",
        "memory"
    ]
    
    results = {}
    for module in modules:
        try:
            __import__(module)
            print(f"  ✓ {module}.py")
            results[module] = True
        except Exception as e:
            print(f"  ✗ {module}.py - {e}")
            results[module] = False
    
    return results

def test_gui_modules():
    """Test GUI modules."""
    print("\n" + "=" * 70)
    print("TESTING GUI MODULES")
    print("=" * 70)
    
    gui_modules = {
        "gui_neural": "Neural GUI (Futuristic)",
        "gui": "Classic GUI",
    }
    
    results = {}
    for module, desc in gui_modules.items():
        try:
            __import__(module)
            print(f"  ✓ {module}.py - {desc}")
            results[module] = True
        except Exception as e:
            print(f"  ✗ {module}.py - {desc} - {e}")
            results[module] = False
    
    return results

def test_optional_modules():
    """Test optional advanced modules."""
    print("\n" + "=" * 70)
    print("TESTING OPTIONAL MODULES")
    print("=" * 70)
    
    optional = {
        "wake_word": "Wake Word Detection",
        "ai_vision": "AI Vision",
        "voice_neural": "Neural Voice",
        "app_control": "App Control"
    }
    
    results = {}
    for module, desc in optional.items():
        try:
            __import__(module)
            print(f"  ✓ {module}.py - {desc}")
            results[module] = True
        except Exception as e:
            print(f"  ⚠ {module}.py - {desc} - Optional (not critical)")
            results[module] = False
    
    return results

def test_file_structure():
    """Test file structure."""
    print("\n" + "=" * 70)
    print("TESTING FILE STRUCTURE")
    print("=" * 70)
    
    required_files = [
        ".env",
        "requirements.txt",
        "README.md",
        "main.py",
        "config.py",
        "brain.py",
        "listen.py",
        "speak.py",
        "tools.py"
    ]
    
    results = {}
    for file in required_files:
        exists = os.path.exists(file)
        results[file] = exists
        status = "✓" if exists else "✗"
        print(f"  {status} {file}")
    
    return results

def test_syntax():
    """Test main.py syntax by compiling it."""
    print("\n" + "=" * 70)
    print("TESTING MAIN.PY SYNTAX")
    print("=" * 70)
    
    try:
        with open("main.py", "r", encoding="utf-8") as f:
            code = f.read()
        compile(code, "main.py", "exec")
        print("  ✓ main.py has no syntax errors")
        return True
    except SyntaxError as e:
        print(f"  ✗ Syntax error in main.py: {e}")
        return False
    except Exception as e:
        print(f"  ✗ Error checking main.py: {e}")
        return False

def main():
    """Run all tests."""
    print("\n")
    print("=" * 60)
    print("     ZEN VOICE ASSISTANT - COMPREHENSIVE SYSTEM TEST")
    print("=" * 60)
    print()
    
    # Run all tests
    import_results = test_imports()
    config_ok = test_config()
    module_results = test_modules()
    gui_results = test_gui_modules()
    optional_results = test_optional_modules()
    file_results = test_file_structure()
    syntax_ok = test_syntax()
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    total_tests = 0
    passed_tests = 0
    
    # Count results
    for results in [import_results, module_results, gui_results, file_results]:
        for result in results.values():
            total_tests += 1
            if result:
                passed_tests += 1
    
    if config_ok:
        passed_tests += 1
    total_tests += 1
    
    if syntax_ok:
        passed_tests += 1
    total_tests += 1
    
    print(f"\nTests Passed: {passed_tests}/{total_tests}")
    
    if passed_tests == total_tests:
        print("\n✓ ALL TESTS PASSED! System is ready to run.")
        print("\nTo start Zen Assistant, run:")
        print("  python main.py")
    else:
        print(f"\n⚠ {total_tests - passed_tests} test(s) failed.")
        print("\nPlease check the errors above and:")
        print("  1. Install missing dependencies: pip install -r requirements.txt")
        print("  2. Verify .env file has correct API keys")
        print("  3. Check for any syntax errors")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
