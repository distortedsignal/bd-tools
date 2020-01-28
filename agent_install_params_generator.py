#! /usr/bin/env python2




'''
Previous template file:

################################################################################
#                        Compute Worker information                            #
# This section is unique per compute worker you want to install.               #
#                                                                              #
# NOTE: Either compute worker section or gateway worker section or k8s host    #
#       host must be uncommented - not all at the same time.                   #
################################################################################
#NODE_TYPE=worker

## Worker IP address
#WORKER=

## Compute worker FQDN. This cannot be changed once the worker is successfully
## added to BlueData cluster. Also, the initialization scripts set the host's
## FQDN to this value if it is not already configured so.
#WORKER_HOSTNAME=

################################################################################
#                         Gateway Worker information                           #
# This section is unique per gateway worker you want to install.               #
#                                                                              #
# NOTE: Either compute worker section or gateway worker section or k8s host    #
#       host must be uncommented - not all at the same time.                   #
################################################################################
#NODE_TYPE=proxy

## Gateway worker IP address
#GATEWAY_NODE_IP=

## Gateway worker FQDN. This cannot be changed once the worker is successfully
## added to BlueData cluster. Also, the initialization scripts set the host's
## FQDN to this value if it is not already configured so.
#GATEWAY_NODE_FQDN=

################################################################################
#                         K8s Host information                                 #
# This section is unique per k8s worker you want to install.                   #
#                                                                              #
# NOTE: Either compute worker section or gateway worker section or k8s host    #
#       host must be uncommented - not all at the same time.                   #
################################################################################
#NODE_TYPE=k8shost

## K8s Worker IP address
#WORKER=

################################################################################
#                             Force installation                               #
# Use this with caution. Forcing an installation when pre-checks failed may    #
# result in an unusable system.                                                #
################################################################################
## Force the installation? 'true' or 'false'
FORCE=false

################################################################################
#                        Installation user and group                           #
# All nodes in the BlueData physical cluster must be installed the same user.  #
# Specify this if the common bundle is not being executed by the same user as  #
# the user that will be running the BlueData services. Please refer to the     #
# System requirements guide for information on permissions required for a      #
# non-root user to install and run BlueData software.                          #
################################################################################
#BLUEDATA_USER=root
#BLUEDATA_GROUP=root

################################################################################
#                         HDFS parameters                                      #
# This is not a common options. It should be uncommented only when tiered      #
# storage was used to configure HDFS (when used as a Tenant Storage).          #
################################################################################
## Report storage type? 'true' or 'false'
#REPORT_STORAGE_TYPE=true

################################################################################
#                         Platform HA not configured                           #
# Ensure the appropriate parameters are uncommented and set in this section    #
# when Platform HA is not enabled.                                             #
################################################################################
## Is PLHA enabled?
#HAENABLED=false

## Controller node's IP address.
#CONTROLLER=

## Controller node's FQDN.
#CONTROLLER_HOSTNAME=

## Controller's unique ID. bdconfig --getvalue bdshared_nodes_controlleruniqueid

################################################################################
#                           Platform HA configured                             #
# Ensure the appropriate parameters are uncommented and set in this section    #
# when Platform HA is enabled.                                                 #
################################################################################
## Is Platform HA enabled?
#HAENABLED=true

## Controller node's IP address. A failover to okay but, his node must be alive
## for a worker to be added.
#CONTROLLER=

## The original shadow controller node's IP address. This node must be alive for
## the worker node to be added.
#SHADOWCTRL=

## The arbiter node's IP address. This node must be alive for the worker node to
## be added.
#ARBITER=

## Controller node's FQDN.
#CONTROLLER_HOSTNAME=

## Shadow controller node's FQDN.
#SHADOW_HOSTNAME=

## Arbiter node's FQDN.
#ARBITER_HOSTNAME=

################################################################################
#                       Miscellaneous parameters                               #
#                                                                              #
################################################################################
## Automount root on the controller node. It must be the same on the worker too.
CONTROLLER_AUTOMOUNT_ROOT=/net/

## Bundle flavor used to install the controller. This may be either 'minimal' or
## 'full'
CONTROLLER_BUNDLE_FLAVOR=minimal

## Skip configuring NTP? 'true' or 'false'
#NO_NTP_CONFIG=false


################################################################################
#                           Network Proxy information                          #
# If the controller was configured with network proxy information, please      #
# specify it here.
################################################################################
#PROXY_URL=
#NO_PROXY=


## UDP port to listen for VXLAN Tunnel packets from other EPIC hosts.
## The port must be the same across all hosts in a EPIC installation. The value
## on the controller can be queried usign `bdconfig --getvalue bds_network_vxlanport`.
## If that query returns nothing, preserve the default.
VXLANPORT=4789

## Controls whether the server should rollback to a clean state when an error
## is encountered during installation. Setting it to 'false' helps with debugging
## but the server should be manually cleaned up before re-attempting the
## installation.
## Values: 'true' or 'false'.
#ROLLBACK_ON_ERROR='false'

# If the controller was configured with --dockerrootsize that is different from 20
# specify it here.
DOCKER_ROOTSIZE=20

## If the controller was upgraded from a version prior to the current one being
## installed, check the output from its
## "bdconfig --getvalue bds_storage_dockersd" command, and supply that value
## here. The current (default) value is "overlay2", and "devicemapper" is the
## other (older) option.
#DOCKER_STORAGE_DRIVER=overlay2

################################################################################
#                        Installation DNSMASQ user and group                   #
# The dnsmasq service needs to run as a user; default user is usually 'nobody'.#
# Specify this if the admin wishes to run dnsmasq as a user other than the     #
# 'nobody:nobody' identity.  The specified user and group must already exist   #
# on the system, and the user must be a member of the specified group.         #
################################################################################
DNSMASQ_USER=nobody
DNSMASQ_GRP=nobody

################################################################################
#                        Internal parameters                                   #
# WARNING: Do not modify these parameters.                                     #
################################################################################
ONWORKER=true
AGENT_INSTALL=true

'''

def greet_user():
    print '''

##############################################
#                                            #
# WELCOME to the Worker Param File Generator #
#                                            #
##############################################

'''

valid_host_choices     = ["1", "2", "3"]
valid_force_choices    = ["1", "2"]
valid_hdfs_choices     = ["1", "2", "3"]
valid_ha_choices       = ["1", "2"]
valid_ntp_config       = ["1", "2", "3"]
valid_rollback_chioces = ["1", "2", "3"]

def get_worker_type():
    while True:
        print '''

What type of worker would you like to install?

###|##############
 1 |        worker
 2 |       gateway
 3 |      k8s_host
'''
        host_choice = raw_input('> ')

        if host_choice in valid_host_choices:
            return host_choice

        print 'Invalid choice - repeating the question'

import socket

def get_choices_for_worker():
    hostname = socket.gethostname()
    ip_addr_str = socket.gethostbyname(hostname)

    return 'NODE_TYPE=worker\nWORKER='+ip_addr_str+'\nWORKER_HOSTNAME='+hostname+'\n'

def get_choices_for_gateway():
    hostname = socket.gethostname()
    ip_addr_str = socket.gethostbyname(hostname)
    
    return 'NODE_TYPE=proxy\nGATEWAY_NODE_IP='+ip_addr_str+'\nGATEWAY_NODE_FQDN='+hostname+'\n'

def get_choices_for_k8s_host():
    hostname = socket.gethostname()
    ip_addr_str = socket.gethostbyname(hostname)
    return 'NODE_TYPE=k8shost\nWORKER='+ip_addr_str+'\n'

def get_install_force():
    while True:
        print '''
Should the installation be forced?
The default is false.

###|######
 1 | false
 2 |  true
'''
        force_choice = raw_input('> ')
        if force_choice in valid_force_choices and (int(force_choice) - 1):
            return 'FORCE=true\n'
        elif force_choice in valid_force_choices and not (int(force_choice) - 1):
            return 'FORCE=false\n'
        else:
            print 'Invalid choice - reprompting'

def get_user_and_group():
    print '''
What user was the controller installed under?
'''
    user_str = raw_input('> ')
    print '''
What group was the controller installed under?
'''
    group_str = raw_input('> ')
    return 'BLUEDATA_USER='+user_str+'\nBLUEDATA_GROUP='+group_str+'\n'

def get_hdfs_params():
    while True:
        print '''
Should HDFS report the storage type?

###|#################
 1 | yes
 2 | no
 3 | omit from config
'''
        hdfs_choice = raw_input('> ')
        if hdfs_choice not in valid_hdfs_choices:
            print 'Invalid choice for hdfs, reprompting.'
            continue

        if hdfs_choice == "3":
            return '\n'
        if hdfs_choice == "2":
            return 'REPORT_STORAGE_TYPE=false\n'
        if hdfs_choice == "1":
            return 'REPORT_STORAGE_TYPE=true\n'

def ha_enabled():
    while True:
        print '''
Is EPIC Platform HA enabled?

###|####
 1 |  no
 2 | yes
'''
        ha_out = raw_input('> ')
        if ha_out not in valid_ha_choices:
            print 'Invalid choice for HA enablement, reprompting.'
            continue

        return bool(int(ha_out) - 1)

def get_controller_params():
    print '''Please input the IP address of the controller
'''
    ip_addr_str = raw_input('> ')

    print '''Please intput the hostname of the controller
'''
    hostname_str = raw_input('> ')
    return 'HAENABLED=false\nCONTROLLER='+ip_addr_str+'\nCONTROLLER_HOSTNAME='+hostname_str+'\n'

def get_ha_controller_params():
    print '''Please input the current (live) controller's IP Address
'''
    controller_ip_addr_str = raw_input('> ')
    print '''Please intput the current shadow controller's IP Address
'''
    shadow_ip_addr_str = raw_input('> ')
    print '''Please input the current arbiter's IP Address
'''
    arbiter_ip_addr_str = raw_input('> ')
    print '''Please input the current (live) controller's hostname
'''
    controller_hostname = raw_input('> ')
    print '''Please input the current shadow's hostname
'''
    shadow_hostname = raw_input('> ')
    print '''Please input the current arbiter's hostname
'''
    arbiter_hostname = raw_input('> ')
    return 'HAENABLED=true\nCONTROLLER='+controller_ip_addr_str+'\nSHADOWCTRL='+shadow_ip_addr_str+\
        '\nARBITER='+arbiter_ip_addr_str+'\nCONTROLLER_HOSTNAME='+controller_hostname+\
        '\nSHADOW_HOSTNAME='+shadow_hostname+'\nARBITER_HOSTNAME='+arbiter_hostname+'\n'

def get_misc_params():
    print '''Please input the automount directory on the controller.
NOTE: this must be the same on ALL hosts.
The default for this is "/net/" - this is probably correct,
but if it is not, please provide the correct directory.
'''
    automount_dir = raw_input('> ')
    if automount_dir == '' or automount_dir == '\n':
        automount_dir = "/net/"

    print '''Please input the controller bundle flavor.
The default is "minimal".
'''
    bundle_flavor = raw_input('> ')
    if bundle_flavor == '' or bundle_flavor == '\n':
        bundle_flavor = "minimal"
    while True:
        print '''Please input the value for the NO_NTP_CONFIG flag.

###|#######
 1 |   true
 2 |  false
 3 | ignore
'''
        ntp_config = raw_input('> ')
        if ntp_config not in valid_ntp_config:
            print 'Not a valid value for NTP config. Reprompting.'
            continue
        if ntp_config == "1":
            return 'CONTROLLER_AUTOMOUNT_ROOT='+automount_dir+'\nCONTROLLER_BUNDLE_FLAVOR='+bundle_flavor+'\nNO_NTP_CONFIG=true\n'
        if ntp_config == "2":
            return 'CONTROLLER_AUTOMOUNT_ROOT='+automount_dir+'\nCONTROLLER_BUNDLE_FLAVOR='+bundle_flavor+'\nNO_NTP_CONFIG=false\n'
        if ntp_config == "3":
            return 'CONTROLLER_AUTOMOUNT_ROOT='+automount_dir+'\nCONTROLLER_BUNDLE_FLAVOR='+bundle_flavor+'\n'

def get_internal_params():
    return 'ONWORKER=true\nAGENT_INSTALL=true\n'

def get_network_parameters():
    print '''Please input the proxy url
'''
    proxy_url = raw_input('> ')
    print '''Please input the no-proxy list
'''
    no_proxy = raw_input('> ')
    print '''Please input the vxlan port.
The default is 4789.
'''
    vxlan_port = raw_input('> ')
    if vxlan_port == '' or vxlan_port == '\n':
        vxlan_port = "4789"
    full_rollback_flag = ''
    while True:
        print '''Please input whether install should be rolled back on errors.

###|######################
 1 | Rollback on errors
 2 | No Rollback on errors
 3 | Ignore
'''
        rollback_chioce = raw_input('> ')
        if rollback_chioce not in valid_rollback_chioces:
            print 'Not a valid value for the Rollback flag. Reprompting.'
            continue

        if rollback_chioce == "1":
            full_rollback_flag += """ROLLBACK_ON_ERROR='true'""" + '\n'
        if rollback_chioce == "2":
            full_rollback_flag += """ROLLBACK_ON_ERROR='false'""" + '\n'
        if full_rollback_flag == "3":
            full_rollback_flag += '\n'

        break

    print '''If the controller was configured with --dockerrootsize
that is different from 20 specify it here.
'''
    docker_root_size = raw_input('> ')

    if docker_root_size == '' or docker_root_size == '\n':
        docker_root_size = "20"

    print '''If the controller was upgraded from a version prior to
the current one being installed, check the output from its
"bdconfig --getvalue bds_storage_dockersd" command, and
supply that value here. The current (default) value
is "overlay2", and "devicemapper" is the other (older) option.'''
    docker_storage_driver = raw_input('> ')
    if docker_storage_driver == '' or docker_storage_driver == '\n':
        docker_storage_driver = 'overlay2'

    network_params_acc = ''

    if proxy_url:
        network_params_acc += 'PROXY_URL='+proxy_url+'\n'

    if no_proxy:
        network_params_acc += 'NO_PROXY='+no_proxy+'\n'

    return network_params_acc+'VXLANPORT='+vxlan_port+'\n'+full_rollback_flag+\
        'DOCKER_ROOTSIZE='+docker_root_size+'\nDOCKER_STORAGE_DRIVER='+\
        docker_storage_driver+'\n'

def get_dnsmasq_values():
    print '''Please input DNSMASQ_USER
The default is "nobody"
'''
    user = raw_input('> ')
    if user == '' or user == '\n':
        user = 'nobody'
    print '''Please input DNSMASQ_GROUP
The default is "nobody"
'''
    group = raw_input('> ')
    if group == '' or group == '\n':
        group = 'nobody'

    return 'DNSMASQ_USER='+user+'\nDNSMASQ_GRP='+group+'\n'

def main():
    greet_user()

    params_file_acc = ''

    host_type_enum = get_worker_type()

    if host_type_enum == "1":
        # We got a worker install
        params_file_acc += get_choices_for_worker()
    if host_type_enum == "2":
        # We got a gateway install
        params_file_acc += get_choices_for_gateway()
    if host_type_enum == "3":
        # We got a k8s host install
        params_file_acc += get_choices_for_k8s_host()

    params_file_acc += get_install_force()

    params_file_acc += get_user_and_group()

    params_file_acc += get_hdfs_params()

    if ha_enabled():
        params_file_acc += get_ha_controller_params()
    else:
        params_file_acc += get_controller_params()

    params_file_acc += get_misc_params()

    params_file_acc += get_network_parameters()

    params_file_acc += get_dnsmasq_values()

    params_file_acc += get_internal_params()

    print '''Output from this program will look like this:

''' + params_file_acc + '''

This will be persisted to the worker.params file.
'''
    f = open('worker.params', 'w')
    f.write(params_file_acc)
    print 'Goodbye.'

if __name__ == '__main__':
    main()
