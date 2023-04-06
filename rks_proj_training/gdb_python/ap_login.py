import paramiko
import time
import store_ap_login 


def wait_remote_shell():
    #sleep for 1 second before uisng the recv
    time.sleep(1)
    while not shell.recv_ready():
        pass

# Prompt the user to enter their username and password
print("Enter below the credentials of the build machine which run this script")
user_bm = input("Enter the username: ")
password_bm = input("Enter the password: ")
ip_bm = input("Enter machine ip:")
print("Enter the program you wish to debug")
prg_name = input()
print("Enter the port number for gdbserver to listen")
gdb_port = input()
print("Enter where your ext_toolpath is")
tool_path = input()

os.chdir(tool_path + 'ext_toolchain_/ext_Toolchain/ap-arm-qca-wsg/tools/3.14.43_gcc-linaro-4.8-2014.04/bin/')
os.putenv('CC', 'arm-linux-uclibcgnueabi-gcc-4.8.3')
os.putenv('AS', 'arm-linux-uclibcgnueabi-as')
os.putenv('LD', 'arm-linux-uclibcgnueabi-ld')
os.putenv('AR', 'arm-linux-uclibcgnueabi-ar')
os.system('./configure')
os.system('make')
# Define the host, username, and password
hosts = store_ap_login.load_hosts()
name, host, user, password = store_ap_login.prompt_hosts(hosts)

# Create a new SSH client object
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# Connect to the remote server
ssh.connect(host, username=user, password=password)

# Open a new shell session
shell = ssh.invoke_shell()
# login prompt followed by enter key
wait_remote_shell()
shell.send(user + '\n')
# Send the password followed by the enter key
wait_remote_shell()
shell.send(password + '\n')
# Send "!v54!" followed by the enter key
wait_remote_shell()
shell.send('!v54!\n')
#whats your chow
wait_remote_shell()
shell.send('\n')
# scp the gdnserver to the AP directory
wait_remote_shell()
shell.send('ls -l\n')

print("Copying gdbserver to AP, PLEASE NOTE if the sshkey of AP<->BuildMachine was not added this call fails. Please copy a dummy file to AP first")
wait_remote_shell()
shell.send('scp -r ' + user_bm + '@' + ip_bm + ':/tmp/hosts.json' + ' /tmp/ ' + '\n')
wait_remote_shell()
shell.send(password_bm + '\n')

wait_remote_shell()
output = shell.recv(2048).decode('utf-8')
print(output)

shell.close()
ssh.close()

