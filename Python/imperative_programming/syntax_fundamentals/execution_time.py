import time
import subprocess
from pathlib import Path

def execute_project_scripts(target_directory):
    base_path = Path(target_directory)
    
    # Recursively find all .py files in the directory
    py_files = list(base_path.rglob("*.py"))
    
    results = []
    start_time_total = time.perf_counter()
    
    for file_path in py_files:
        # Extract relative path (e.g., python\imperative_programming\...) for clean display
        try:
            rel_path = file_path.relative_to(base_path.parent)

        except ValueError:
            rel_path = file_path.name
            
        start_time_file = time.perf_counter()
        
        try:
            # Execute the file. 
            # timeout = 2 is critical here to prevent scripts with input() loops from freezing the execution.
            process = subprocess.run(
                ["python", str(file_path)],
                capture_output = True,
                text = True,
                timeout = 2
            )

            status = "PASS" if process.returncode == 0 else "FAIL"

        except subprocess.TimeoutExpired:
            status = "TIMEOUT"  # Flags interactive files requiring user input

        except Exception:
            status = "ERROR" # Flags unexpected errors during execution 
            
        end_time_file = time.perf_counter()
        exec_time = end_time_file - start_time_file
        
        results.append((str(rel_path), status, exec_time))
        
    end_time_total = time.perf_counter()
    total_time = end_time_total - start_time_total
    
    # Generate Pytest-style ASCII Table
    print("\n" + "=" * 60 + " execution report " + "=" * 60)
    print(f"{'Name':<105} {'Status':<15} {'Time'}")
    print("-" * 138)
    
    for name, status, t in results:
        print(f"{name:<105} {status:<15} {t:>6.3f}s")
        
    print("-" * 138)
    print(f"TOTAL FILES: {len(results):<93} TOTAL TIME: {total_time:.2f}s")
    print("=" * 138 + "\n")

if __name__ == "__main__":
    # Insert specific absolute path
    TARGET_DIR = r"C:\Users\A.I.M\C.S\Data-Science-Project\python"
    
    execute_project_scripts(TARGET_DIR)

