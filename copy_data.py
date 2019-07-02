import paramiko
from scp import SCPClient\

ADDR='10.249.77.131'

ssh_client=paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=ADDR,username='pi',password='raspberry')

stdin,stdout,stderr=ssh_client.exec_command('ls')
print(stdout.readlines())

scp_client = SCPClient(ssh_client.get_transport())
scp_client.get('~/Downloads/test.png','/root/workspace/CV/YOLOv3-Object-Detection-with-OpenCV/')
