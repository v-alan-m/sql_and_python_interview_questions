import os
import sys
import subprocess

def run_tests():
    print("Executing Pytest test suite...")
    print("-" * 50)
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    tests_dir = os.path.join(current_dir, "tests")
    
    if not os.path.exists(tests_dir):
        print(f"Error: Tests folder '{tests_dir}' does not exist.")
        return False
        
    try:
        # Run pytest via subprocess. Check_call throws exception on non-zero exit code
        result = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v"], cwd=current_dir)
        return result.returncode == 0
    except Exception as e:
        print(f"Critical error invoking pytest: {e}")
        return False

if __name__ == "__main__":
    success = run_tests()
    if not success:
        sys.exit(1)
    else:
        print("\nAll tests passed successfully!")
        sys.exit(0)
