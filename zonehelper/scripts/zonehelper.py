#!/usr/bin/env python


from zonehelper.zonehelper import get_commands, save_commands


def main():
    storage_host_commands, storage_initiator_commands, switch_commands = \
            get_commands()
    save_commands('output/create_host_cmd', storage_host_commands)
    save_commands('output/create_initiator_cmd', storage_initiator_commands)
    save_commands('output/create_switch_cmd', switch_commands)


if __name__ == '__main__':
    main()
