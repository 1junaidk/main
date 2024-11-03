from netmiko import ConnectHandler
import difflib

# Device config
device = {
    'device_type': 'cisco_ios',
    'ip': '192.168.56.101',       
    'username': 'prne',        
    'password': 'cisco123!',    
    'secret': 'class123!' 
}

# Connect to the device
connection = ConnectHandler(**device)
connection.enable()  

# Retrieve running configuration
running_config = connection.send_command('show running-config')
# Retrieve startup configuration
startup_config = connection.send_command('show startup-config')

# Save running configuration to a file
with open('running_config.txt', 'w') as run_file:
    run_file.write(running_config)

# Save startup configuration to a file
with open('startup_config.txt', 'w') as start_file:
    start_file.write(startup_config)

# Disconnect from the device
connection.disconnect()

# Print confirmation
print("Configs retrieved and stored successfully.")

# Function to compare configurations
def compare_configs(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        # Read lines from both files
        running_lines = f1.readlines()
        startup_lines = f2.readlines()
        
        # Use difflib to get the difference
        diff = difflib.unified_diff(
            running_lines, 
            startup_lines, 
            fromfile='Running Config', 
            tofile='Startup Config', 
            lineterm=''
        )
        
        # Display the differences line by line
        print("\nDifferences between Running and Startup Configurations:\n")
        for line in diff:
            print(line)

# Call the compare function
compare_configs('running_config.txt', 'startup_config.txt')




from netmiko import ConnectHandler

# Define device and syslog server IP
device = {
    'device_type': 'cisco_ios',
    'ip': '192.168.56.101',       
    'username': 'prne',        
    'password': 'cisco123!',     
    'secret': 'class123!' 
}
syslog_server_ip = "192.168.56.101"  

# Connect to the device
connection = ConnectHandler(**device)
connection.enable()  

# Configure the device to enable syslog
commands = [
    f"logging host {syslog_server_ip}",
    "logging trap informational",     # Set the logging level to informational
    "logging on"                      # Enable logging
]
output = connection.send_config_set(commands)

# Disconnect from the device
connection.disconnect()

# Print the output to confirm the configuration
print("Syslog configuration output:\n", output)
print(f"Syslog configured to send logs to {syslog_server_ip}.")

hardening_checks = {
    "SSH enabled": "ip ssh version 2",
    "Telnet disabled": "no service telnet",
    "Password encryption": "service password-encryption",
    "Logging enabled": "logging buffered",
    "NTP configured": "ntp server"
}

def check_hardening(running_config):
    for check, rule in hardening_checks.items():
        if rule in running_config:
            print(f"[PASS] {check}")
        else:
            print(f"[FAIL] {check}")

check_hardening(running_config)
