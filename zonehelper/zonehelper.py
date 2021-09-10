import yaml
import prompt
import re


def get_hosts_info(path):
    return yaml.safe_load(open(path))


def get_user_input(user_message):
    return prompt.string(user_message)


def get_storage_initiator_cmd(hostname, pwwn, port, server_type, host_id, sp_mode_type):
    return 'create initiator fc wwn={0} alias={1}_{2}_p{3} multipath_type=third-party failover_mode=special_mode special_mode_type={4} path_type=optimized host_id={5}\n'.format(pwwn, server_type, hostname, port, sp_mode_type, host_id)


def get_storage_initiator_dorado_v6_cmd(hostname, pwwn, port, server_type, host_id):
    return 'create initiator fc wwn={0} alias={1}_{2}_p{3} multipath_type=default host_id={4}\n'.format(pwwn, server_type, hostname, port, host_id)


def get_storage_host_cmd(hostname, os_type, server_ip, host_id):
    return 'create host name={0} operating_system={1} ip={2} host_id={3}\n'.format(hostname, os_type, server_ip, host_id)


def get_san_cmd(pwwn, hostname, server_type, port):
    return 'device-alias name {0}_{1}_p{2} pwwn {3}\n'.format(server_type, hostname, port, pwwn)


def get_pwwn_storage_style(pwwn):
    regex = r'(\w\w):(\w\w):(\w\w):(\w\w):(\w\w):(\w\w):(\w\w):(\w\w)'
    match = re.match(regex, pwwn)
    return ''.join([match.group(i) for i in range(1, 9)]) if match else pwwn


def get_pwwn_san_style(pwwn):
    regex = r'(\w\w)(\w\w)(\w\w)(\w\w)(\w\w)(\w\w)(\w\w)(\w\w)'
    match = re.match(regex, pwwn)
    return ':'.join([match.group(i) for i in range(1, 9)]) if match else pwwn


def save_commands(filename, commands):
    with open(filename, 'w') as f:
        f.writelines(commands)


def get_commands():
    path_to_hosts = get_user_input('Enter hosts config file: ')
    hosts_parsed = get_hosts_info(path_to_hosts)
    storage_is_dorado_v6 = True if get_user_input('Enter Yes if Dorado V6, else No: ') == 'Yes' else False
    os_type = get_user_input('Enter hosts OS (VMware_ESX or Linux): ')
    host_id = get_user_input('Enter first empty host_id: ')
    server_type = get_user_input('Enter server type (SB or SR): ')
    sp_mode_type = 'mode1' if os_type == 'VMware_ESX' else 'mode0'
    storage_initiator_commands = []
    storage_host_commands = []
    san_commands = []
    for hostname in hosts_parsed.keys():
        server_ip = hosts_parsed[hostname]['ip']
        create_host_cmd = get_storage_host_cmd(hostname, os_type, server_ip, host_id)
        storage_host_commands.append(create_host_cmd)
        for index, pwwn in enumerate(hosts_parsed[hostname]['pwwn']):
            port = str(index + 1)
            pwwn_storage_style = get_pwwn_storage_style(pwwn)
            if storage_is_dorado_v6:
                create_initiator_cmd = get_storage_initiator_dorado_v6_cmd(hostname, pwwn_storage_style, port, server_type, host_id)
            else:
                create_initiator_cmd = get_storage_initiator_cmd(hostname, pwwn_storage_style, port, server_type, host_id, sp_mode_type)
            storage_initiator_commands.append(create_initiator_cmd)
            pwwn_san_style = get_pwwn_san_style(pwwn)
            create_san_cmd = get_san_cmd(pwwn_san_style, hostname, server_type, port)
            san_commands.append(create_san_cmd)
        host_id = str(int(host_id) + 1)
    save_commands('output/create_host_cmd', storage_host_commands)
    save_commands('output/create_initiator_cmd', storage_initiator_commands)
    save_commands('output/create_san_cmd', san_commands)
