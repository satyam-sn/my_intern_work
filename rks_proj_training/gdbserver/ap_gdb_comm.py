
import os
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

print('Enter where your toopath is:')
# specify the path to the directory that contains the ext_toolchain_ directory
tool_path = input()

# read the profile names from a text file
with open("profiles1.txt", "r") as f:

    valid_profiles = [line.strip() for line in f.readlines()]

print("Valid profile names:", valid_profiles)

# get the profile name from the user
profile_name = input("Enter a profile name: ").strip()

# check if the profile name is valid
if profile_name not in valid_profiles:
    raise ValueError("Invalid profile name: {}".format(profile_name))

# construct the full path to the directory based on the profile name
full_path = os.path.join(tool_path, "ext_toolchain_", "ext_Toolchain", profile_name, "tools", "3.14.43_gcc-linaro-4.8-2014.04", "bin")
gdbserver_path =  os.path.join(tool_path, "ext_toolchain_", "ext_Toolchain", profile_name, "build", "3.14.43_gcc-linaro-4.8-2014.04", "toolchain_build_arm_release","gdb-7.8.1","gdb","gdbserver","gdbserver")

if 'gdbserver' in os.listdir(os.path.dirname(gdbserver_path)):
    print('gdbserver file exists')
else:
    print('gdbserver file does not exist')

# change the current working directory to the full path
    os.chdir(full_path)

# print the current working directory to confirm it was changed correctly
    print("Current working directory:", os.getcwd())
    os.chdir(full_path)
    CC = os.path.join(full_path,'arm-linux-uclibcgnueabi-gcc-4.8.3')
    AS = os.path.join(full_path, 'arm-linux-uclibcgnueabi-as')
    LD = os.path.join(full_path, 'arm-linux-uclibcgnueabi-ld')
    AR = os.path.join(full_path, "arm-linux-uclibcgnueabi-ar")
    os.putenv('CC', CC)
    os.putenv('AS', AS)
    os.putenv('LD', LD)
    os.putenv('AR', AR)
    parent_path = os.path.dirname(gdbserver_path)
    os.chdir(parent_path )
    os.system('./configure --host=arm-linux-gnueabi')
    os.system('make')
    print("Current working directory:", os.getcwd())
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
wait_remote_shell()
shell.send('ls -l\n')

print("Copying gdbserver to AP, PLEASE NOTE if the sshkey of AP<->BuildMachine was not added this call fails. Please copy a dummy file to AP first")
wait_remote_shell()
if 'gdbserver' in os.listdir(os.path.dirname(gdbserver_path)):
    print('gdbserver file exists')
else:
    print('gdbserver file does not exist')
    gdbserver_path=":" + gdbserver_path
    shell.send('scp -r ' + user_bm + '@' + ip_bm + gdbserver_path + ' /writable/ ' + '\n')
    wait_remote_shell()
    shell.send(password_bm + '\n')
    
wait_remote_shell()
output = shell.recv(2048).decode('utf-8')
print(output)

shell.send(f"ps -ef | grep {prg_name} | grep -v grep | awk '{{print $2}}'\n")

time.sleep(1)

output = shell.recv(65535).decode("utf-8")

pid = output.strip()

port_number = input("Enter port number for gdbserver (default 1234): ") or "1234"
shell.send(f"/writable/gdbserver :{port_number} --attach {pid}\n")

time.sleep(1)

output = shell.recv(65535).decode("utf-8")

print(output)

shell.close()
ssh.close()

