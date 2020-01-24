#! /usr/bin/python

import os
import subprocess
import sys

cmd_list = ['/usr/local/bin/erlc', '-W']
include_dir_list = [
    '/Users/tom/Documents/src/BlueData/everest/mgmt/shared/bd_shared/include',
    '/Users/tom/Documents/src/BlueData/everest/mgmt/shared/bd_shared/legacy_include',
    '/Users/tom/Documents/src/BlueData/everest/mgmt/controller/server/bd_throttle/include',
    '/Users/tom/Documents/src/BlueData/everest/mgmt/controller/server/bd_hypervisor_controller/legacy_include',
    '/Users/tom/Documents/src/BlueData/everest/mgmt/controller/server/bd_hypervisor_controller/include',
    '/Users/tom/Documents/src/BlueData/everest/mgmt/controller/server/bd_kube_authn/include',
    '/Users/tom/Documents/src/BlueData/everest/mgmt/controller/server/bd_util/include',
    '/Users/tom/Documents/src/BlueData/everest/mgmt/controller/server/bd_mgmt/include',
    '/Users/tom/Documents/src/BlueData/everest/mgmt/controller/server/bd_mgmt/legacy_include',
    '/Users/tom/Documents/src/BlueData/everest/mgmt/controller/server/bd_hypervisor_agent/include',
    '/Users/tom/Documents/src/BlueData/everest/mgmt/controller/server/bd_os_client/include',
    '/Users/tom/Documents/src/BlueData/everest/mgmt/controller/server/deps/mochiweb/test',
    '/Users/tom/Documents/src/BlueData/everest/mgmt/controller/server/deps/mochiweb/include',
    '/Users/tom/Documents/src/BlueData/everest/mgmt/controller/server/deps/mochiweb/examples/hmac_api',
    '/Users/tom/Documents/src/BlueData/everest/mgmt/controller/server/deps/esaml/include',
    '/Users/tom/Documents/src/BlueData/everest/mgmt/controller/server/deps/esaml/src',
    '/Users/tom/Documents/src/BlueData/everest/mgmt/controller/server/deps/uuid/src',
    '/Users/tom/Documents/src/BlueData/everest/mgmt/controller/server/bd_ha/include',
    '/Users/tom/Documents/src/BlueData/everest/mgmt/vm/vagent/bd_vagent/include',
    '/Users/tom/Documents/src/BlueData/everest/io/base/tools/bds_io_bqs/include',
    '/Users/tom/Documents/src/BlueData/everest/io/base/ct',
    '/Users/tom/Documents/src/BlueData/everest/io/base/apps/bds_memq/include',
    '/Users/tom/Documents/src/BlueData/everest/io/base/apps/data_server/include',
    '/Users/tom/Documents/src/BlueData/everest/io/base/apps/bd_logger/include',
    '/Users/tom/Documents/src/BlueData/everest/mgmt/controller/server/deps/esaml/include',
    '/Users/tom/Documents/src/BlueData/everest/mgmt/controller/server/deps/esaml/src'
]
cmd_out_dir_list = ['-o', '/tmp']

comment_sequence = '%'

def main():
    args = sys.argv[1:]
    include_list_with_flag_tuples = zip(['-I']*len(include_dir_list), include_dir_list)
    include_list_with_flag = [i for tup in include_list_with_flag_tuples for i in tup]
    cmd_list.extend(include_list_with_flag)
    cmd_list.extend(cmd_out_dir_list)

    walk_output = next(os.walk(args[0]))

    filenames = walk_output[2]

    for f_name in filenames:
        filepath = os.path.join(os.getcwd(), args[0], f_name)
        with open(filepath, 'r') as source_file:
            file_content = source_file.read()

        if file_content.find('-include(') == -1:
            continue

        print f_name
        file_lint_command = list(cmd_list)
        file_lint_command.append(filepath)

        try:
            lint_command_good_output = subprocess.check_output(file_lint_command)
        except:
            continue

        file_lines = file_content.split('\n')
        new_file = list(file_lines)

        include_lines = []

        for counter, line in enumerate(file_lines):
            if line.find('-include(') > -1:
                include_lines.append(counter)

        for index in include_lines:
            new_file[index] = comment_sequence + ' ' + new_file[index]
            with open(filepath, 'w') as source_file:
                source_file.write('\n'.join(new_file))

            try:
                maybe_good_cmd_out = subprocess.check_output(file_lint_command)

                if maybe_good_cmd_out == lint_command_good_output:
                    continue
            except subprocess.CalledProcessError:
                new_file[index] = file_lines[index]

        with open(filepath, 'w') as source_file:
            source_file.write('\n'.join(new_file))


if __name__ == "__main__":
    main()
