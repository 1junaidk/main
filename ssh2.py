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

# Device connection details
device = {
    'device_type': 'cisco_ios',
    'ip': '192.168.56.101',  # Replace with device IP
    'username': 'prne',  # Replace with device username
    'password': 'cisco123!',  # Replace with device password
}

try:
    # Connect to device
    net_connect = ConnectHandler(**device)

    # Retrieve running and startup configurations
    running_config = net_connect.send_command('show running-config').splitlines()
    startup_config = net_connect.send_command('show startup-config').splitlines()
    print("running config:", running_config)
    print("startup config:", startup_config)
    # Close connection
    net_connect.disconnect()

    # Compare running and startup configs
    print("Differences between Running and Startup Configurations:")
    diff = difflib.unified_diff(startup_config, running_config, fromfile='Startup Config', tofile='Running Config', lineterm='')
    
    diff_output = list(diff)
    if not diff_output:
        print("No differences found.")
    else:
        for line in diff_output:
            print(line)

    # Hardening compliance checks
    print("\nHardening Compliance Checks:")
    hardening_issues = []

    # Check for SSH configuration (looks for any 'transport input ssh' command on all vty lines)
    if not any('transport input ssh' in line for line in running_config):
        hardening_issues.append("Warning: SSH is not enabled!")

    # Check for Telnet disabled
    if any('transport input telnet' in line for line in running_config):
        hardening_issues.append("Warning: Telnet is enabled! Disable it for security.")

    # Check for logging configuration
    if not any('logging' in line for line in running_config):
        hardening_issues.append("Warning: Logging is not configured.")

    # Output hardening issues
    if hardening_issues:
        print("\nHardening Issues Found:")
        for issue in hardening_issues:
            print(issue)
    else:
        print("All basic hardening checks passed.")

except Exception as e:
    print(f"An error occurred: {e}")