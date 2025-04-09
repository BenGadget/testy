import paramiko
import getpass

def ssh_connect(ip, username, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Accept unknown host keys
        client.connect(ip, username=username, password=password)
        print(f"✅ Successfully connected to {ip}")

        while True:
            command = input("Enter command to run (or type 'exit' to quit): ")
            if command.strip().lower() == "exit":
                print("🔌 Disconnecting...")
                break

            stdin, stdout, stderr = client.exec_command(command)
            output = stdout.read().decode()
            error = stderr.read().decode()

            print("\n📤 Command Output:")
            print(output if output else "(No output)")
            if error:
                print("\n❌ Errors:")
                print(error)

        client.close()
        print("Disconnected.")

    except Exception as e:
        print(f"🚨 Failed to connect: {e}")

if __name__ == "__main__":
    ip = input("🔗 Enter the IP address to connect to: ")
    #username = input("👤 Enter your SSH username: ")
    #password = getpass.getpass("🔑 Enter your SSH password: ")
    username = "admin"
    password = "NECTARY-checkers-divers"

    
    ssh_connect(ip, username, password)
    exec_command("execute backup config tftp 2025-04-09.config 10.83.83.196")