from argparse_prompt import PromptParser

import config
from client import create_directory, transfer_ansible_folder, deploy_ansible, cleanup_remote_files

def main(args):
  # Setup variables
  cfg = config.load()
  credentials = (args.user, args.password)
  # iterate over execution nodes
  for e_node in cfg['execution_hosts']: #TODO: add parallal processing
    # Create remote path string
    remote_path = e_node['remote_path']
    if remote_path[-1] == '/':
      remote_path = remote_path[0:(len(remote_path)-1)]
    remote_path = remote_path + "/ansible_remote_temp"
    # Create folder on execution node
    create_directory(e_node, credentials, remote_path)
    # Transfer ansbile files
    transfer_ansible_folder(e_node, credentials, remote_path)
    # Envoke ansible-runner
    stdout, stderr = deploy_ansible(e_node, credentials, remote_path)
    # Print output. Keep in mind this provides info after it runs. It does not provide live output.
    if stdout:
      print(stdout)
    if stderr:
      print(stderr)
    # Clean up transferred files
    cleanup_remote_files(e_node, credentials, remote_path)


if __name__=="__main__":
  # Utilizes PromptParser to avoid logging user credentials in history.
  argparser = PromptParser()

  # Add the arguments
  argparser.add_argument('-u',
                        '--user',
                        help='Username to login to servers')
  argparser.add_argument('-p',
                        '--password',
                        help='Password to login to servers')
  # Execute the parse_args() method
  args = argparser.parse_args()

  main(args)