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

print('Enter where your toolpath is:')

# specify the path to the directory that contains the ext_toolchain_ directory
tool_path = input()

# read the profile names from a text file
with open("ap_profile.txt", "r") as f:

    valid_profiles = [line.strip() for line in f.readlines()]

print("Valid profile names:", valid_profiles)

# get the profile name from the user
profile_name = input("Enter a profile name: ").strip()

# check if the profile name is valid
if profile_name not in valid_profiles:
    raise ValueError("Invalid profile name: {}".format(profile_name))

# construct the full path to the directory based on the profile name
profile_path = os.path.join(tool_path, "ext_toolchain_", "ext_Toolchain", profile_name, "tools")
files = os.listdir(profile_path)
directory_name = files[0]
full_path = os.path.join(profile_path, directory_name, "bin")
gdbserver_path =  os.path.join(tool_path, "ext_toolchain_", "ext_Toolchain", profile_name, "build", directory_name, "toolchain_build_arm_release","gdb-7.8.1","gdb","gdbserver","gdbserver")

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
#shell.send('ls -l\n')

print("Copying gdbserver to AP, PLEASE NOTE if the sshkey of AP<->BuildMachine was not added this call fails. Please copy a dummy file to AP first")
wait_remote_shell()
shell.send("test -e /writable/gdbserver && echo 'File exists' || echo 'File does not exist'\n")
wait_remote_shell()

output = shell.recv(65535).decode("utf-8").strip()
print(output)

#Check for gdbserver file on AP side
if output.count("File exists") == 2:
    print("File exists on remote server")
else:
    print("File does not exist on remote server")
    gdbserver_path=":" + gdbserver_path
    shell.send('scp -r ' + user_bm + '@' + ip_bm + gdbserver_path + ' /writable/ ' + '\n')
    wait_remote_shell()
    shell.send(password_bm + '\n')
    wait_remote_shell()

shell.send('ps -ef |' +'grep'+' ' + prg_name + "| grep -v grep | awk  '{print $1}' | head -n 1"+'\n')
wait_remote_shell()
output = shell.recv(2048).decode("utf-8")
print(output)
pid = output.splitlines()[1]
print(pid)
port_number = input("Enter port number for gdbserver (default 1234): ") or "1234"
shell.send(f"/writable/gdbserver :{port_number} --attach {pid}\n")
wait_remote_shell()
output = shell.recv(65535).decode("utf-8")
print(output)

print("Current working directory:", os.getcwd())

#check if the current working directory has the buildroot directory
if "buildroot" in os.getcwd():
    buildr_path = os.getcwd()
    buildroot_path = os.path.join(buildr_path, "build", profile_name, "build_arm_release")
else:
    buildr_path = input("Please enter the path to the buildroot directory: ")
    buildroot_path = os.path.join(buildr_path, "build", profile_name, "build_arm_release")

print("Buildroot path:", buildroot_path)

#Check for directory of not stripped files 
dst_dir = os.path.join("/home/administrator/",profile_name,"root")
if  os.path.exists(dst_dir):
    print(f"The destination directory for not stripped library already exist at {dst_dir}")
else :
    print(f"The destination directory for not stripped library doesnt  exist at {dst_dir}")
    os.makedirs(dst_dir)
   
    # Find all .so files and check if they are stripped
    files = os.popen(f'find {buildroot_path} -name "*.so"').read().splitlines()
    for file in files:
        os.system(f"file {file} > {file}.out")
        with open(f"{file}.out", "r") as f:
             file_content = f.read()
             if "not stripped" in file_content:
                 os.system(f"cp {file} {dst_dir}")

    print(f"Copy operation completed successfully. Copied all unstripped '.so' files from {buildroot_path} to {dst_dir}.")

os.chdir(full_path)
os.system('./arm-linux-uclibcgnueabi-gdb')
shell.close()
ssh.close()


