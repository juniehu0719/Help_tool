import os
import platform
import shutil
import socket
import subprocess
from datetime import datetime

try:
    import psutil
except ImportError:
    print("psutil is not installed. Run: pip install psutil")
    raise


def print_header():

    print("IT System Monitoring & Troubleshooting Tool")
    print(f"Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"System: {platform.system()} {platform.release()}")


def check_cpu():
    cpu_percent = psutil.cpu_percent(interval=1)
    print("\n[CPU USAGE]")
    print(f"Current CPU Usage: {cpu_percent}%")

    if cpu_percent < 50:
        print("Status: Normal")
       
        print("Status: Moderate")
        
    else:
        print("Status: High")
       


def check_memory():
    mem = psutil.virtual_memory()
    print("\n[MEMORY USAGE]")
    print(f"Used: {mem.percent}%")
    print(f"Available: {round(mem.available / (1024**3), 2)} GB")

    if mem.percent < 60:
        print("Status: Normal")
        
    elif mem.percent < 85:
        print("Status: Moderate")
        
    else:
        print("Status: High")
       


def check_disk():
    total, used, free = shutil.disk_usage("/")
    used_percent = (used / total) * 100

    print("\n[DISK SPACE]")
    print(f"Total: {round(total / (1024**3), 2)} GB")
    print(f"Used: {round(used / (1024**3), 2)} GB")
    print(f"Free: {round(free / (1024**3), 2)} GB")
    print(f"Usage: {used_percent:.2f}%")

    if used_percent < 70:
        print("Status: Normal")
      
    elif used_percent < 90:
        print("Status: Moderate")
       
    else:
        print("Status: Critical")
        


def check_network():
    print("\n[NETWORK CONNECTIVITY]")
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        print("Status: Connected")
       
    except OSError:
        print("Status: Disconnected")
        

def ping_test():
    print("\n[PING TEST]")
    host = "8.8.8.8"

    if platform.system().lower() == "windows":
        command = ["ping", "-n", "2", host]
    else:
        command = ["ping", "-c", "2", host]

    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"Ping to {host} successful.")
        else:
            print(f"Ping to {host} failed.")
            print("Recommendation: Network may be unstable or blocked.")
    except Exception as e:
        print(f"Ping test error: {e}")







def main():
    print_header()
    check_cpu()
    check_memory()
    check_disk()
    check_network()
    ping_test()
    


if __name__ == "__main__":
    main()