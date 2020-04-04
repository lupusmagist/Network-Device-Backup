from netmiko import ConnectHandler
import paramiko


def Device_Backup(ipaddress, username, password, SSHPort, device_type):
    # Main backup call, depending on device type, gets backup
    if device_type == 'MIKROTIK':
        command = 'export compact'
        return SSHBackup(ipaddress, username, password, SSHPort, command)
    elif device_type == 'UBNTRADIO':
        command = 'cat /tmp/system.cfg'
        return SSHBackup(ipaddress, username, password, SSHPort, command)
    elif device_type == 'HP':
        command = 'show running-config'
        return EnableBackup(ipaddress, username, password, SSHPort, command)
    else:
        raise ValueError("Device Type not found.")


def SSHBackup(ipaddress, username, password, SSHPort, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ipaddress, SSHPort, username, password)

        stdin, stdout, stderr = ssh.exec_command("print")
        stdin, stdout, stderr = ssh.exec_command(command)
        outlines = stdout.readlines()
        resp = ''.join(outlines)
        # print(resp)
        ssh.close()
        return resp
    except paramiko.ssh_exception.AuthenticationException:
        # We will just log errors
        print("Authentication Failed - " + ipaddress)
    except paramiko.ssh_exception.BadAuthenticationType:
        # We will just log errors
        print("Authentication Type Fail - " + ipaddress)
    except paramiko.ssh_exception.NoValidConnectionsError:
        # We will just log errors
        print("Connection Error - " + ipaddress)


def EnableBackup(ipaddress, username, password, SSHPort, command):
    net_connect = ConnectHandler(device_type='hp_procurve', ip=ipaddress,
                                 username=username, password=password)
    resp = net_connect.send_command(command)
    net_connect.disconnect()
    return resp
