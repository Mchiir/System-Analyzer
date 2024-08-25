import platform
import os
import socket
import urllib.request
import shutil
import psutil
import os
from collections import defaultdict
import time

def system_details():
    def identify_os():
        os_name = platform.system()
        os_release = platform.release()
        if os_name == "Windows":
            return f"Operating System: {os_name} {os_release}"
        elif os_name == "Linux":
            try:
                import distro  # Importing the distro library for detailed Linux info
                distro_name = distro.name() or "Unknown Linux"
            except ImportError:
                distro_name = "Unknown Linux"
            return f"Operating System: {distro_name} {os_release}"
        elif os_name == "Darwin":
            return f"Operating System: macOS {os_release}"
        else:
            return f"Operating System: {os_name} {os_release}"

    print(identify_os())
    node = platform.uname().node
    version = platform.uname().version
    machine = platform.uname().machine
    print(f"Node name: {node}, OS version: {version}, Machine baseSystem: {machine}")


def get_private_ip():
    hostname = socket.gethostname()
    private_ip = socket.gethostbyname(hostname)
    return private_ip

def get_public_ip():
    public_ip = urllib.request.urlopen("https://api.ipify.org").read().decode('utf8')
    return public_ip

def get_default_gateway():
    gateways = psutil.net_if_addrs()
    default_gateway = psutil.net_if_stats()
    for interface, addrs in gateways.items():
        if interface in default_gateway:
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    return addr.address
    return None

if __name__ == "__main__":
    gateway = get_default_gateway()

def get_parent_directory():
    current_path = os.getcwd()
    parent_path = os.path.dirname(current_path)
    if os.name == 'nt':  # windows
        drive, _ = os.path.splitdrive(parent_path)
        return drive + '/'
    else:  # Linux and macOS
        return parent_path

parent_directory = get_parent_directory()

def get_disk_usage():
    path = parent_directory
    
    if not os.path.exists(path):
        print("The specified path does not exist.")
        return
    
    print("Disk usage data: ")
    total, used, free = shutil.disk_usage(path)
    print(f"Total: {total / (1024 ** 3):.2f} GB")
    print(f"Used: {used / (1024 ** 3):.2f} GB")
    print(f"Free: {free / (1024 ** 3):.2f} GB")


def get_top5_largest_dir():
    def get_directory_sizes(start_path):
        dir_sizes = defaultdict(int)

        for dirpath, dirnames, filenames in os.walk(start_path):
            try:
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    dir_sizes[dirpath] += os.path.getsize(filepath)
            except (PermissionError, FileNotFoundError) as e:
                print(f"Error accessing {dirpath}: {e}")
                continue

        return dir_sizes

    def largest_directories(start_path, top_n=5):
        dir_sizes = get_directory_sizes(start_path)
        largest_dirs = sorted(dir_sizes.items(), key=lambda x: x[1], reverse=True)[:top_n]
        return largest_dirs

    def bytes_to_gb(bytes_size):
        return bytes_size / (1024 * 1024 * 1024)

    if __name__ == "__main__":
        path = parent_directory

        if os.path.exists(path) and os.path.isdir(path):
            # temporary message
            print("Calculating largest directories, please wait...", end='', flush=True)

            largest_dirs = largest_directories(path)

            print("\r" + " " * 50 + "\r", end='')  # line clearing
            print("Largest directories:")

            for directory, size in largest_dirs:
                size_gb = bytes_to_gb(size)
                print(f"{directory}: {size_gb:.2f} GB")
        else:
            print("No directory found.")


def cpu_time_monitoring():
    def monitor_cpu_usage(interval=1):
        try:
            while True:
                cpu_usage = psutil.cpu_percent(interval=interval)
                print(f"CPU Usage: {cpu_usage}%")
        except KeyboardInterrupt:
            print("Monitoring stopped.")

    if __name__ == "__main__":
        print("Monitoring CPU usage. Press Ctrl+C to stop.")
        monitor_cpu_usage()


def cpu_once_monitoring():
    def display_cpu_usage():
        cpu_usage = psutil.cpu_percent(interval=1)
        print(f"CPU Usage: {cpu_usage}%")

    if __name__ == "__main__":
        print("Displaying CPU usage once.")
        display_cpu_usage()
    # cpu_prompt_monitoring()

def manual():
    def choos():
        print("\nWelcome! Here's the collection of data about the system.")
        print("Enter: ")
        print("system : to see system specific details")
        print("private : to see system private Ip")
        print("public : to see system public Ip")
        print("gateway : to see default gateway")
        print("disk : to see Disk space usage percentages")
        print("largest : to display the first five directories in given path")
        print("cpu : to display cpu Monitoring values")
        print("all: to get all information")

        choice = input("Enter your choice: ").strip().lower()
        print('\n')
        if choice in ['', 'system']:
            system_details()
        elif choice in 'private':
            print("Private IP Address:", get_private_ip())
        elif choice in 'public':
            print("Public IP Address:", get_public_ip())
        elif choice in 'gateway':
            print("Default Gateway:", gateway)
        elif choice in 'disk':
            get_disk_usage()
        elif choice in 'largest':
            get_top5_largest_dir()
        elif choice in 'cpu':
            cpu_time_monitoring()
        elif choice in 'all':
            system_details()
            print("Private IP Address:", get_private_ip())
            print("Public IP Address:", get_public_ip())
            print("Default Gateway:", gateway)
            get_disk_usage()
            get_top5_largest_dir()
            cpu_time_monitoring()
        else:
            print("\nProgram exit")
            SystemExit
        print('\n')

    choos()
    while True:
        c = input("Want to continue? [Yes/No]: ").strip().lower()
        if c not in ['', 'y', 'yes']:
            print('Bye\n')
            break
        else:
            choos()

def automatic():
    
    while True:
        system_details()
        print("Private IP Address:", get_private_ip())
        print("Public IP Address:", get_public_ip())
        print("Default Gateway:", gateway)
        print('\n')
        get_disk_usage()
        print('\n')
        get_top5_largest_dir()
        print('\n')
        cpu_once_monitoring()
        print('\nEnter ctrl+c to exit\n')
        time.sleep(10)
        os.system('cls')
        

print("Welcome to LOG ANALYZER!")
choose = input("Do you want automatic[Yes] or manual system[No]: ").strip().lower()

if choose in ['y', 'yes']:
    automatic()
else:
    manual()