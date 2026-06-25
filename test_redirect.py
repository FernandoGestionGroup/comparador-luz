import os
import sys

def run_with_redirect():
    # File descriptor for stdout
    fd = sys.stdout.fileno()
    
    # Save the original fd
    saved_fd = os.dup(fd)
    
    # Open devnull
    devnull = os.open(os.devnull, os.O_WRONLY)
    
    # Overwrite stdout with devnull
    os.dup2(devnull, fd)
    
    try:
        # This print goes to devnull
        print("This should be hidden", flush=True)
        os.write(1, b"This C-level write should be hidden\n")
    finally:
        # Restore original stdout
        os.dup2(saved_fd, fd)
        os.close(devnull)
        os.close(saved_fd)

run_with_redirect()
print("This should be visible")
os.write(1, b"This C-level write should be visible\n")
