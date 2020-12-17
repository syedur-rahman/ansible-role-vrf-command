""" command filter
contains all the jinja2 custom filters for show command manipulation """

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

class FilterModule(object):
    """ filter module
    required class for ansible to implement custom jinja2 filters """
    
    def filters(self):
        filters = {
            'update_with_vrfs': update_with_vrfs,
        }
        return filters