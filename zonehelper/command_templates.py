STORAGE_INITIATOR_CMD = ('create initiator fc '
                         'wwn={0} '
                         'alias={1}_{2}_p{3} '
                         'multipath_type=third-party '
                         'failover_mode=special_mode '
                         'special_mode_type={4} '
                         'path_type=optimized host_id={5}\n')

STORAGE_INITIATOR_DORADO_V6_CMD = ('create initiator fc '
                                   'wwn={0} '
                                   'alias={1}_{2}_p{3} '
                                   'multipath_type=default '
                                   'host_id={4}\n')

STORAGE_HOST_CMD = ('create host '
                    'name={0} '
                    'operating_system={1} '
                    'ip={2} '
                    'host_id={3}\n')

SAN_CMD = ('device-alias '
           'name {0}_{1}_p{2} '
           'pwwn {3}\n')
