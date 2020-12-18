""" command filter
contains all the jinja2 custom filters for show command manipulation """

def check_for_vrfs(vrf_commands):
    """ check for vrfs
    check through the vrf commands to see if user requested vrf updates """

    # set up the flag
    vrfs_required = False

    # iterate through the user provided commands
    for command in vrf_commands:
        # if the user provided vrf aware syntax
        if '<vrf>' in command:
            vrfs_required = True
            break

    return vrfs_required

def update_with_vrfs(vrf_commands, vrfs):
    """ update with vrfs
    updates the vrf commands with the collected vrf data """

    # initialize updated vrf commands
    updated_vrf_commands = []

    # iterate through the user provided commands
    for command in vrf_commands:
        # if the user provided vrf aware syntax
        if '<vrf>' in command:
            # iterate through the collected vrfs
            for vrf in vrfs:
                # skip default vrfs provided on nxos devices
                # the global table commands are accounted for in the 
                # later half of this function
                if vrf == 'default':
                    continue

                # update the command with the vrf
                updated_command = command.replace('<vrf>', vrf)

                # add the updated command to the updated vrf commands
                updated_vrf_commands.append(updated_command)

            # also add the global table vrsion of the command
            updated_command = command.replace('vrf <vrf>', '').strip()
            updated_command = updated_command.replace('  ', ' ')

            # add the updated command to the updated vrf commands
            updated_vrf_commands.append(updated_command)

        # otherwise add the command unmodified
        else:
            updated_vrf_commands.append(command)

    return updated_vrf_commands

def clean_up_command_output(raw_command_data):
    """ clean up command output
    restructures the registered output data """

    # initialize vrf command output
    vrf_command_output = []

    # skip if no data available in the raw command data
    if 'results' not in raw_command_data:
        return vrf_command_output

    # otherwise iterate through the raw command data
    for result in raw_command_data['results']:
        # initialize relevant values
        command = result['item']
        failed = result['failed']
        output = ''

        # save the output if there was no failure in execution
        if 'stdout' in result:
            # update output
            output = result['stdout'][0]
        # save failure message as well in case command failed to execute
        elif 'msg' in result:
            # update output
            output = result['msg']

        # show command information
        show_command_info = {
            'command': command,
            'output': output,
            'failed': failed,
        }

        # append show command information to vrf command output
        vrf_command_output.append(show_command_info)

    return vrf_command_output

class FilterModule(object):
    """ filter module
    required class for ansible to implement custom jinja2 filters """
    
    def filters(self):
        filters = {
            'check_for_vrfs': check_for_vrfs,
            'update_with_vrfs': update_with_vrfs,
            'clean_up_command_output': clean_up_command_output,
        }
        return filters