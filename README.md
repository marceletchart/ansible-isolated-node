# ansible-isolated-node.py
Run ansible cli against isolated nodes to reach distant hosts. Similar to how AWX/Ansible Tower uses isolated nodes.
## Note
This is mostly an experiment but if something useful comes of it then feel free to use it.
## Usage
- Design ansible playbooks/roles to operate as if running from execution node.  
- Recommended to use a separate inventory files per execution node (assuming execution nodes are in network segmented environments)
- Fill out config.yml with ansible playbook/role info per execution node.
Then run:
```
cd ansible-remote/
python main.py
```
The tool will prompt you for your username and password
* username: The user used to login to your remote systems used as isolated/execution nodes
* password: The password used to login to your remote systems used as isolated/execution nodes

## Requirements
* On localhost
```
pip install -r requirements.txt
```
* On execution nodes:
```
pip install ansible-runner --user

# For windows hosts
pip install pywinrm
```
## Future Plans
Feel free to request additional features! 
- [] Update to install as a package
- [] Support sshkey authentication
- [] Parallel processing for multiple execution nodes
- [] Stream real-time ansible task updates from execution nodes. (maybe as a flag option?)
