from zonehelper.command_templates import \
        STORAGE_INITIATOR_CMD, \
        STORAGE_INITIATOR_DORADO_V6_CMD, \
        STORAGE_HOST_CMD, \
        SAN_CMD
from zonehelper.parser import get_hosts_info
import prompt
import re


def get_user_input(user_message):
    return prompt.string(user_message)


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


def get_params():
    dorado_v6 = True \
            if get_user_input('Enter Yes if Dorado V6, else No: ') == 'Yes' \
            else False
    os_type = get_user_input('Enter hosts OS (VMware_ESX or Linux): ')
    host_id = get_user_input('Enter start host_id: ')
    server_type = get_user_input('Enter server type (SB or SR): ')
    sp_mode_type = 'mode1' if os_type == 'VMware_ESX' else 'mode0'
    path_to_hosts = get_user_input('Enter hosts config file: ')
    return (path_to_hosts, dorado_v6, os_type, host_id, server_type, sp_mode_type)


def get_commands():
    path_to_conf, dorado_v6, os_type, host_id, server_type, sp_mode_type = \
            get_params()
    hosts_parsed = get_hosts_info(path_to_conf)
    storage_initiator_commands = []
    storage_host_commands = []
    switch_commands = []
    for hostname in hosts_parsed.keys():
        server_ip = hosts_parsed[hostname]['ip']
        create_host_cmd = STORAGE_HOST_CMD.format(hostname, os_type, server_ip, host_id)
        storage_host_commands.append(create_host_cmd)
        for index, pwwn in enumerate(hosts_parsed[hostname]['pwwn']):
            port = str(index + 1)
            pwwn_storage_style = get_pwwn_storage_style(pwwn)
            if dorado_v6:
                create_initiator_cmd = STORAGE_INITIATOR_DORADO_V6_CMD.format(pwwn_storage_style, server_type, port, host_id)
            else:
                create_initiator_cmd = STORAGE_INITIATOR_CMD.format(pwwn_storage_style, server_type, hostname, port, sp_mode_type, host_id)
            storage_initiator_commands.append(create_initiator_cmd)
            pwwn_san_style = get_pwwn_san_style(pwwn)
            create_switch_cmd = SAN_CMD.format(server_type, hostname, port, pwwn_san_style)
            switch_commands.append(create_switch_cmd)
        host_id = str(int(host_id) + 1)
    return storage_host_commands, storage_initiator_commands, switch_commands
