import pexpect
ip_address = '192.168.56.101'
username = 'prne'
password = 'cisco123!'
password_enable = 'class123!'

session = pexpect.spawn('ssh ' + username + '@' + ip_address,
                        encoding='utf-8', timeout=20)
result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])

if result != 0:
    print('---FAILURE! creating sesison for: ', ip_address)
    exit()

session.sendline(password)
result = session.expect(['>', pexpect.TIMEOUT, pexpect.EOF])

if result != 0:
    print('---FAILURE NACAS! entering password: ', password)
    exit()

session.sendline('enable')
result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])

if result != 0:
    print('----FAILURE! entering enable mode')
    exit()

session.sendline(password_enable)
result = session.expect(['#', pexpect.TIMEOUT, pexpect.EOF])

if result != 0:
    print('---FAILURE! entering enable mode after sending password')
    exit()

session.sendline('configure terminal')
result = session.expect([r'.\(config\)#', pexpect.TIMEOUT, pexpect.EOF])

if result != 0:
    print('---FAILURE entering config mode')
    exit()

session.sendline('hostname R1')
result = session.expect([r'R1\(config\)#', pexpect.TIMEOUT, pexpect.EOF])

if result != 0:
   print('---FAILURE! setting hostname')

session.sendline('exit')

session.sendline('exit')

print('----------------------------')
print('')
print('---SUCCESS! connecting to : ', ip_address)
print('---                  Username: ', username)
print('-----                Password: ', password)
print('')
print('-----------------------------')

session.close()
