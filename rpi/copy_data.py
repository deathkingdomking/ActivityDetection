import paramiko
from scp import SCPClient

ADDR='sha-51764-mbp.local'

ssh_client=paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=ADDR,username='Dakan Wang',password='WeWork1203')

stdin,stdout,stderr=ssh_client.exec_command('ls')
print(stdout.readlines())

scp_client = SCPClient(ssh_client.get_transport())
scp_client.put('/home/pi/Downloads/test.png','/Users/dakanwang/Downloads/')
