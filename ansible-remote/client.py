import paramiko
from scp import SCPClient

def create_directory(host_cfg, credentials, remote_path):
  """Creates the remote_path on the provided remote host."""
  try:
    ssh = _createSSHClient(host_cfg['hostname'], '22', credentials(0), credentials(1))
    ssh.exec_command('mkdir -p {}'.format(remote_path))
    ssh.close()
  except Exception as e:
    raise SystemExit("Failed to create path: {} on remote host: {}. \nError: {}".format(remote_path, host_cfg['hostname'], e))

def transfer_ansible_folder(host_cfg, credentials, remote_path):
  """Transfers the ansible folder to the execution host."""
  try:
    scp = _setup_scp(host_cfg['hostname'], credentials)
    scp.put(host_cfg["local_ansible_folder"], recursive=True, remote_path=remote_path)
  except Exception as e:
    raise SystemExit("Failed to transfer local files in path: {} to remote host: {}. \nError: {}".format(host_cfg["local_ansible_folder"], host_cfg['hostname'], e))


def deploy_ansible(host_cfg, credentials, remote_path):
  """Runs ansible-runner with provided ansible code on the execution host."""
  ssh = _createSSHClient(host_cfg['hostname'], '22', credentials(0), credentials(1))
  stdin, stdout, stderr = ssh.exec_command('ansible-runner run {} --inventory {} -p {}'.format(remote_path, host_cfg["inventory"], host_cfg["playbook"]))
  return stdout.read().decode(), stderr.read().decode()

def cleanup_remote_files(host_cfg, credentials, remote_path):
  """Deletes files in the remote_path on the provided remote host."""
  try:
    ssh = _createSSHClient(host_cfg['hostname'], '22', credentials(0), credentials(1))
    ssh.exec_command('rm -rf {}'.format(remote_path))
    ssh.close()
  except Exception as e:
    raise SystemExit("Failed to delete path: {} on remote host: {}. \nError: {}".format(remote_path, host_cfg['hostname'], e))

def _setup_scp(node, credentials):
  """Sets up scp connection"""
  ssh = _createSSHClient(node, '22', credentials(0), credentials(1))
  scp = SCPClient(ssh.get_transport())
  return scp

def _createSSHClient(server, port, user, password):
  """Creates SSH client to be used for scp and exec_command"""
  client = paramiko.SSHClient()
  client.load_system_host_keys()
  client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  client.connect(server, port, user, password)
  return client
