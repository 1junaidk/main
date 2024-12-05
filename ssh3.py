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

print("Configuring OSPF...")
ospf_output = connection.send_config_set(ospf_commands)
print(ospf_output)

# Save the configuration
print("Saving configuration...")
save_output = connection.send_command("write memory")
print(save_output)

print("Disconnected from the router.")
connection.disconnect()


