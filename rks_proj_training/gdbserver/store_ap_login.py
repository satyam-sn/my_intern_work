import json

HOSTS_FILE = "hosts.json"

# Load host information from file
def load_hosts():
    try:
        with open(HOSTS_FILE, "r") as f:
            hosts = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        hosts = {}
    return hosts

# Save host information to file
def save_hosts(hosts):
    with open(HOSTS_FILE, "w") as f:
        json.dump(hosts, f)

# Display menu and prompt for user input
def prompt_hosts(hosts):
    while True:
        print("Available hosts:")
        for i, name in enumerate(hosts.keys()):
            print(f"{i+1}. {name}")
        print("0. Add new host")

        choice = input("Select a host: ")
        if choice == "0":
            name = input("Enter host name: ")
            ip = input("Enter host IP: ")
            username = input("Enter username: ")
            password = input("Enter password: ")
            hosts[name] = {"ip": ip, "username": username, "password": password}
            save_hosts(hosts)
            print(f"Host '{name}' added.")
        elif choice.isdigit():
            index = int(choice) - 1
            if index >= 0 and index < len(hosts):
                name = list(hosts.keys())[index]
                host = hosts[name]
                return name, host["ip"], host["username"], host["password"]
        print("Invalid choice. Please try again.")
