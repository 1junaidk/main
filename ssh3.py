# Import the required modules
import pexpect

# Define variables
ip_address = '192.168.56.101' # ip adress of the remote device
username = 'prne'                                                                           #SSH username for the login
password = 'cisco123!'                                                                      #SSH password for authentication
password_enable = 'class123!'                                                               #Password to enter enable mode

# Initiates the SSH session
session = pexpect.spawn('ssh ' + username + '@' + ip_address, encoding='utf-8', timeout=60) #Spawn function starts the ssh connection to the remote device
result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])                        #Encoding function ensures that text is sent and recieved
                                                                                            #Timeout=60 means there is a minure timeout for the operation
# Check for error, if exists then display error and exit
if result != 0:                                                                             #If statement checks where statment is true, if true executes the code in the block
    print('--- FAILURE! creating session for: ', ip_address)                                #Result is a variable which stores the value of session.expect, '!=' is not equal to '0' is true
    exit()

# Session expecting password, enter details
session.sendline(password)                                                                  #Script sends the stored password to complete ssh login
result = session.expect(['>', pexpect.TIMEOUT, pexpect.EOF])                                #If the prompt '>' is returned it means it was succesful

# Check for error, if exists then display error and exit
if result != 0:                                                                             #Confirms that  login was successful. If there is an incorrect password or timeoutit prints error message and exits.                                            
    print('--- FAILURE! entering password: ', password)
    exit()

# Enter enable mode
session.sendline('enable')                                                                  #Enable command enters into privileged mode which allows access to configuration commands
result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])                        #If password doesnt appear in the timeout period set the function will reture pexpect.TIMEOUT

# Check for error, if exists then display error and exit
if result != 0:                                                                             #As mentioned previously same function with different variables 
    print('--- Failure! entering enable mode')
    exit()

# Send enable password details
session.sendline(password_enable)                                                           #Enters the enable password, if '#' is receieved indicates succesfull access to enable mode
result = session.expect(['#', pexpect.TIMEOUT, pexpect.EOF])

# Check for error, if exists then display error and exit
if result != 0:                                                                             #This block ensures that the enable password was accepted. If not, the script exits with an error message.
    print('--- Failure! entering enable mode after sending password')
    exit()

# Enter configuration mode
session.sendline('configure terminal')                                                      #Send the configure terminal command, when '(config)# is returned it signals it was succesful
result = session.expect([r'.\(config\)#', pexpect.TIMEOUT, pexpect.EOF])

# Check for error, if exists then display error and exit
if result != 0:                                                                             #This block verifies that the router has successfully entered configuration mode. If not, an error message is printed, and the script exits.
    print('--- Failure! entering config mode')
    exit()

# Print the IP address, username, and password
print('--------------------------------------------------')                                 #Printing the IP address, username, and both passwords (login and enable). It acts as a confirmation of successful login and privilege escalation.
print('Connection Details:')
print(f'--- Success! Connecting to: {ip_address}')
print(f'---                        Username: {username}')
print(f'---                          Password: {password}')
print(f'---              Enable Password: {password_enable}')
print('--------------------------------------------------')

# Change the hostname to Router1
session.sendline('hostname Router1')                                                        #It waits for the updated prompt, which should include Router1(config)# if the hostname change is successful.
result = session.expect([r'Router1\(config\)#', pexpect.TIMEOUT, pexpect.EOF])

# Check for error, if exists the display error and exit
if result != 0:                                                                             #This block checks whether the hostname change was successful. If not, an error message is printed.
    print('--- Failure! setting hostname')

#print('--------------------------')                                                        #attempted a no shutdown function however does not work
#print('Please select an option:')
#print('1. No Shutdown interface')
#print('2. Shutdown interface')

#user_choice = input('1 or 2: ')

#if user_choice != 1:
    #print('Carrying out no shutdown interface')
    #session.sendline('GigabitEthernet0/0')
    #session.expect([r'GigabitEthernet0/0\(config\#', pexpect.TIMEOUT, pexpect.EOF])

#if result != 0:
    #session.sendline('no shutdown')
    #session.expect([r'GigabitEthernet0/0\(config\#', pexpect.TIMEOUT, pexpect.EOF])

#if result != 0:
#print('---Interface GigabitEthernet0/0 enabled successfully')

#else:
  #print('---Failed to enable interface')
  #user_choice = input('Enter your choice: ')

#if user_choice != 2:
    #print('Executing shutdown interface')
    #session.sendline('GigabitEthernet0/0')
    #session.expect([r'GigabitEthernet0/0\(config\#', pexpect.TIMEOUT, pexpect.EOF])

# Exit enable mode
session.sendline('exit')

# Terminate SSH session
session.close() 



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


# --------------- Remote device configuration ---------------- #

from netmiko import ConnectHandler

router = {
    'device_type': 'cisco_ios',
    'host': '192.168.56.101',
    'username': 'prne',
    'password': 'cisco123!',
    'secret': 'class123!',
}

print("Connecting to the router...")
connection = ConnectHandler(**router)
connection.enable()
print("Connection to the router successful, entering privileged mode.")

commands = [
    'interface Loopback0',
    'ip address 192.168.1.1 255.255.255.255',
    'description Loopback Interface',
    'interface GigabitEthernet2',
    'ip address 1.1.1.1 255.255.255.0',
    'description LAN Interface',
    'no shutdown',
    'ip route 0.0.0.0 0.0.0.0 10.0.0.2',
]

print("Configuring Loopback0...")
output = connection.send_config_set(commands)
print(output)

ospf_commands = [
    'router ospf 1',  # Start OSPF process
    'network 192.168.1.1 0.0.0.0 area 0',  # Advertise Loopback0
    'network 1.1.1.0 0.0.0.255 area 0',  # Advertise GigabitEthernet2
    'passive-interface Loopback0',  # Passive for Loopback0
]

print("Configuring OSPF.")
ospf_output = connection.send_config_set(ospf_commands)
print(ospf_output)

# Save the configuration
print("Saving configuration.")
save_output = connection.send_command("write memory")
print(save_output)

print("Disconnected from the router.")
connection.disconnect()


