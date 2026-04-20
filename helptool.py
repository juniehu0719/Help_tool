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
        print("Recommendation: CPU usage is healthy.")
    elif cpu_percent < 80:
        print("Status: Moderate")
        print("Recommendation: Close unnecessary background applications if system feels slow.")
    else:
        print("Status: High")
        print("Recommendation: High CPU usage detected. Check running processes and close heavy programs.")


def check_memory():
    mem = psutil.virtual_memory()
    print("\n[MEMORY USAGE]")
    print(f"Used: {mem.percent}%")
    print(f"Available: {round(mem.available / (1024**3), 2)} GB")

    if mem.percent < 60:
        print("Status: Normal")
        print("Recommendation: Memory usage is healthy.")
    elif mem.percent < 85:
        print("Status: Moderate")
        print("Recommendation: Consider closing unused applications to free memory.")
    else:
        print("Status: High")
        print("Recommendation: High memory usage detected. Restart heavy apps or reboot the system.")


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
        print("Recommendation: Disk space is sufficient.")
    elif used_percent < 90:
        print("Status: Moderate")
        print("Recommendation: Delete unnecessary files and clear downloads/trash.")
    else:
        print("Status: Critical")
        print("Recommendation: Disk space is very low. Remove large files immediately.")


def check_network():
    print("\n[NETWORK CONNECTIVITY]")
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        print("Status: Connected")
        print("Recommendation: Internet connection appears to be working.")
    except OSError:
        print("Status: Disconnected")
        print("Recommendation: No internet connection detected. Check Wi-Fi/Ethernet and router.")


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


def show_top_processes():
    print("\n[TOP 5 CPU PROCESSES]")
    processes = []

    for proc in psutil.process_iter(["pid", "name", "cpu_percent"]):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    processes = sorted(processes, key=lambda x: x["cpu_percent"], reverse=True)

    for proc in processes[:5]:
        print(f"PID: {proc['pid']:<8} Name: {proc['name']:<25} CPU: {proc['cpu_percent']}%")


def generate_summary():
    print("\n[SUMMARY]")
    cpu_percent = psutil.cpu_percent(interval=1)
    mem_percent = psutil.virtual_memory().percent
    total, used, free = shutil.disk_usage("/")
    disk_percent = (used / total) * 100

    issues = []

    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
    except OSError:
        issues.append("No internet connection")

    if cpu_percent >= 80:
        issues.append("High CPU usage")
    if mem_percent >= 85:
        issues.append("High memory usage")
    if disk_percent >= 90:
        issues.append("Low disk space")

    if not issues:
        print("No major issues detected. System appears healthy.")
    else:
        print("Detected issues:")
        for issue in issues:
            print(f"- {issue}")


def main():
    print_header()
    check_cpu()
    check_memory()
    check_disk()
    check_network()
    ping_test()
    show_top_processes()
    generate_summary()
    print("\nScan complete.")


if __name__ == "__main__":
    main()