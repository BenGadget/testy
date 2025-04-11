import paramiko
import getpass
import datetime

results = open("results.txt","w")
dayDate = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
file = open("switches.txt","r")


def ssh_connect(ip, username, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Accept unknown host keys
        client.connect(ip, username=username, password=password)
        print(f"✅ Successfully connected to {ip}")

        # Automatically run backup command first
        backup_cmd = f"execute backup config tftp {ip}-{dayDate}.config 10.83.83.3"
        print(f"\n📦 Running backup command: `{backup_cmd}`")
        stdin, stdout, stderr = client.exec_command(backup_cmd)
        print("\n📤 Backup Output:")
        print(stdout.read().decode())
        error = stderr.read().decode()
        if error:
            print("\n❌ Backup Errors:")
            print(error)

        # Then enter interactive loop for custom commands
        #while True:
        #   command = input("\n💻 Enter a command to run (or type 'exit' to quit): ")
        #    if command.strip().lower() == "exit":
        #        print("🔌 Disconnecting...")
        #        break
        #
        #    stdin, stdout, stderr = client.exec_command(command)
        #    output = stdout.read().decode()
        #    error = stderr.read().decode()
        #
        #    print("\n📤 Command Output:")
        #    print(output if output else "(No output)")
        #    if error:
        #        print("\n❌ Errors:")
        #        print(error)

        client.close()
        print("🚪 Disconnected.")

    except Exception as e:
        print(f"🚨 Failed to connect: {e}")


for line in file:
    # Split the line into IP and credentials
    parts = line.strip().split(",")
    if len(parts) == 3:
        ip, username, password = parts
        ip = ip.strip()
        username = username.strip()
        password = password.strip()

        # Print the extracted information
        print(f"IP: {ip}") # Username: {username}, Password: {password}")

        ssh_connect(ip, username, password)
    
        # Write to results file
        results.write(f"IP: {ip}, Username: {username}, Password: {password}\n")
    else:
        print("Invalid line format. Expected format: IP,Username,Password")
file.close()
# Close the results file


#if __name__ == "__main__":
    #ip = input("🔗 Enter the IP address to connect to: ")
    #username = input("👤 Enter your SSH username: ")
    #password = getpass.getpass("🔑 Enter your SSH password: ")
    #ip = "10.82.82.12"
    #username = "admin"
    #password = "NECTARY-checkers-divers"
    
#    ssh_connect(ip, username, password)
