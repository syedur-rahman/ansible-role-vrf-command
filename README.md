# vrf_command

This Ansible Network role provides the ability to send VRF-aware network commands to network devices dynamically. Currently, this is supported on IOS / EOS / NXOS devices.

The role is intended to be an enhancement of the default behavior of the following modules:

- `ios_command`
- `nxos_command`
- `eos_command`

## Requirements

None.

## Role Variable

The following value that should be updated based on your requirements (see `defaults/main.yml`):

```yaml
vrf_command_list:
  - "show ip route vrf <vrf>"
  - "show version"
```

The `vrf_command_list` should be updated to include all commands that the you wish to run against your network devices. To make a command behave in a **VRF-aware** manner, use the syntax `<vrf>` within the command.

Note that you can run regular non-VRF related commands as well.

## Output Variable

The role generates a custom output variable for user convenience called `vrf_command_output`.

The format of the data structure is as follows:

```yaml
vrf_command_output:
  - command: "show ip route vrf dev"
  	failed: False
  	output: "...77.77.77.0 is directly connected, FastEthernet1/0\n..." (omitted)
  - command: "show blah blah"
  	failed: True
  	output: "...% Invalid input detected at..." (omitted)

```

The data structure returns a list of values. Within each list are three keys.

- `command` - The show command that was run against the network device.
- `failed` - Boolean where `true` is command failed and `false` is command executed successfully.
- `output` - The output of the show command.

## Example Playbook 1

The below example playbook demonstrates basic usage on how the role can be used.

```yaml
- hosts: all

  vars:
    vrf_command_list:
      - "show ip interface brief vrf <vrf>"
      - "show ip route vrf <vrf>"
      - "show interface status"
      - "show version"
      
  roles:
  	- syedur_rahman.vrf_command
```

## Example Playbook 2

The below example playbook demonstrates manipulating the `vrf_command_output` to dump to text files.

```yaml
- hosts: all

  vars:
    vrf_command_list:
      - "show ip route vrf <vrf>"
      
  roles:
  	- syedur_rahman.vrf_command
  	
- hosts: localhost

  tasks:
  - template:
      src: "show_command.j2"
      dest: "{{ item }}.txt"
    loop: "{{ groups['all'] }}"
```

With the below being the `show_command.j2` template.

```jinja2
{% for show_command_info in hostvars[item]['vrf_command_output'] %}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
{{ show_command_info['command'] }}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
{{ show_command_info['output'] }}
{% endfor %}
```

This results in the following type of output per device.

```
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
show ip route vrf management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
IP Route Table for VRF "management"
'*' denotes best ucast next-hop
'**' denotes best mcast next-hop
'[x/y]' denotes [preference/metric]
'%<string>' in via output denotes VRF <string>

192.168.12.0/24, ubest/mbest: 1/0, attached
    *via 192.168.12.135, mgmt0, [0/0], 05:12:12, direct
192.168.12.135/32, ubest/mbest: 1/0, attached
    *via 192.168.12.135, mgmt0, [0/0], 05:12:12, local

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
show ip route
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
IP Route Table for VRF "default"
'*' denotes best ucast next-hop
'**' denotes best mcast next-hop
'[x/y]' denotes [preference/metric]
'%<string>' in via output denotes VRF <string>

2.2.2.0/24, ubest/mbest: 1/0, attached
    *via 2.2.2.2, Lo100, [0/0], 05:12:28, direct
2.2.2.2/32, ubest/mbest: 1/0, attached
    *via 2.2.2.2, Lo100, [0/0], 05:12:28, local
2.3.4.0/24, ubest/mbest: 1/0, attached
    *via 2.3.4.5, Lo23, [0/0], 05:12:28, direct
2.3.4.5/32, ubest/mbest: 1/0, attached
    *via 2.3.4.5, Lo23, [0/0], 05:12:28, local
```

## License

MIT

## Author Information

This role was created in 2020 by Syedur Rahman.