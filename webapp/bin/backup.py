from netmiko import ConnectHandler
import paramiko
from webapp import db
from webapp.models.logging import Logging
import socket


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
        log = Logging(log="Backup made for - " +
                      ipaddress, log_type="SUCCESS")
        db.session.add(log)
        db.session.commit()
        return resp
    except paramiko.ssh_exception.AuthenticationException:
        # We will just log errors
        # print("Authentication Failed - " + ipaddress)
        log = Logging(log="Authentication Failed for - " +
                      ipaddress, log_type="ERROR")
        db.session.add(log)
        db.session.commit()
        return -1
    except paramiko.ssh_exception.BadAuthenticationType:
        # We will just log errors
        # print("Authentication Type Fail - " + ipaddress)
        log = Logging(log="Authentication Type Fail for - " +
                      ipaddress, log_type="ERROR")
        db.session.add(log)
        db.session.commit()
        return -1
    except paramiko.ssh_exception.NoValidConnectionsError:
        # We will just log errors
        # print("Connection Error - " + ipaddress)
        log = Logging(log="Connection Error to - " +
                      ipaddress, log_type="ERROR")
        db.session.add(log)
        db.session.commit()
        return -1
    except socket.error:
        # We will just log errors
        # print("Socket Error - " + ipaddress)
        log = Logging(log="Cant connect to - " + ipaddress, log_type="ERROR")
        db.session.add(log)
        db.session.commit()
        return -1


def EnableBackup(ipaddress, username, password, SSHPort, command):
    net_connect = ConnectHandler(device_type='hp_procurve', ip=ipaddress,
                                 username=username, password=password)
    resp = net_connect.send_command(command)
    net_connect.disconnect()
    return resp
