import os
import sys
import traceback

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tests.test_pipeline as test_module


def run_all_tests():
    test_functions = [
        getattr(test_module, name)
        for name in dir(test_module)
        if name.startswith("test_")
    ]

    passed = 0
    failed = 0

    print("Running tests...")
    print("=" * 50)

    for test_func in test_functions:
        try:
            test_func()
            print(f"{test_func.__name__} ... PASSED")
            passed += 1
        except Exception:
            print(f"{test_func.__name__} ... FAILED")
            traceback.print_exc()
            failed += 1

    print("=" * 50)
    print(f"Total: {passed + failed}, Passed: {passed}, Failed: {failed}")


if __name__ == "__main__":
    run_all_tests()
