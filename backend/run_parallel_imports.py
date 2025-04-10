import subprocess
import sys
import os

def run_parallel_imports(total_artists=140000, num_processes=4, batch_size=100):
    """
    Run multiple artist import processes in parallel
    """
    print(f"Starting {num_processes} parallel import processes for {total_artists} artists...")
    
    # Calculate artists per process
    artists_per_process = total_artists // num_processes
    
    processes = []
    
    for i in range(num_processes):
        start_offset = i * artists_per_process
        limit = artists_per_process if i < num_processes - 1 else total_artists - start_offset
        
        # Build the command
        cmd = [
            sys.executable,
            "manage.py",
            "fetch_artists",
            "--limit", str(limit),
            "--batch-size", str(batch_size),
            "--start-offset", str(start_offset),
            "--process-id", str(i+1),
            "--rate-limit", "0.5"  # Try a slightly faster rate limit
        ]
        
        # Start the process
        print(f"Starting process {i+1} with offset {start_offset}, limit {limit}")
        process = subprocess.Popen(cmd)
        processes.append(process)
    
    # Wait for all processes to complete
    for i, process in enumerate(processes):
        process.wait()
        print(f"Process {i+1} completed with exit code {process.returncode}")
    
    print("All import processes completed!")

if __name__ == "__main__":
    # Get command line arguments
    total_artists = int(sys.argv[1]) if len(sys.argv) > 1 else 100000
    num_processes = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    batch_size = int(sys.argv[3]) if len(sys.argv) > 3 else 100
    
    run_parallel_imports(total_artists, num_processes, batch_size)