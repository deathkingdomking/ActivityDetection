import paramiko
from scp import SCPClient

ADDR='10.249.77.157'
USR_NAME='Dakan Wang'
PWD = 'WeWork1203'


class SSH_Client:
  def __init__(self):
    self.ssh_client=paramiko.SSHClient()
    self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


  def copy_to_server(self, in_folder, out_folder):    
    self.ssh_client.connect(hostname=ADDR,username=USR_NAME,password=PWD)
    print ('connecting to on_prem_server using ssh')
    stdin,stdout,stderr=self.ssh_client.exec_command('ls')
    print(stdout.readlines())
    scp_client = SCPClient(self.ssh_client.get_transport())
    scp_client.put(in_folder, recursive=True, remote_path=out_folder)
    
