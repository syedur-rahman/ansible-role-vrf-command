""" vrf filter
contains all the jinja2 custom filters for vrf data manipulation """

def parse_nxos_vrfs(raw_vrf_data):
    """ parse nxos vrfs
    takes the raw nxos 'show vrf' command output and
    parses through it for the vrf names """

    # initialize vrfs list
    # this will contain all the vrfs on the device
    vrfs = []

    # set up capture vrf flag
    # this will be used to determine when to start capturing vrf name data
    # from the raw vrf command output
    capture_vrf = False

    # iterate through the raw vrf data
    for line in raw_vrf_data['stdout_lines'][0]:
        # skip empty lines
        if not line.strip():
            continue

        # set capture flag upon reaching a standard header attribute
        if 'vrf-name' in line.lower() and capture_vrf != True:
            capture_vrf = True
            continue

        # start capturing vrf name data
        if capture_vrf:
            # capture when these key words show up in the line
            if 'down' in line.lower() or 'up' in line.lower():
                # capture vrf name
                vrf = line.split()[0]

                # add vrf name to the vrfs list
                vrfs.append(vrf)

    return vrfs

def parse_ios_vrfs(raw_vrf_data):
    """ parse ios vrfs
    takes the raw ios 'show ip vrf' or 'show vrf' command output and 
    parses through it for the vrf names """

    # initialize vrfs list
    # this will contain all the vrfs on the device
    vrfs = []

    # set up capture vrf flag
    # this will be used to determine when to start capturing vrf name data
    # from the raw vrf command output
    capture_vrf = False

    # set up the exact column location of the header
    column_location = 0

    # set the margin of error for vrf name location
    error_margin = 3

    # iterate through the raw vrf data
    for line in raw_vrf_data['stdout_lines'][0]:
        # skip empty lines
        if not line.strip():
            continue

        # set capture flag upon reaching a standard header attribute
        if 'name' in line.lower() and capture_vrf != True:
            capture_vrf = True

            # also set the column location of the header
            column_location = len(line.rstrip()) - len(line.strip())

            continue

        # start capturing vrf name data
        if capture_vrf:
            # set the vrf line column location
            vrf_line_column_location = len(line.rstrip()) - len(line.strip())

            # capture the vrf name assuming the name shows up in the same
            # relative position with a bit of an error margin as the header
            # otherwise assume this is a multi-line output; only really
            # required for ios as ios has no easy keywords to determine 
            # whether the line contains a vrf name when using 'show ip vrf'
            if vrf_line_column_location <= ( column_location + error_margin ):
                # capture vrf name
                vrf = line.split()[0]

                # add vrf name to the vrfs list
                vrfs.append(vrf)

    return vrfs

def parse_eos_vrfs(raw_vrf_data):
    """ parse eos vrfs
    takes the raw eos 'show vrf' command output and
    parses through it for the vrf names """

    # initialize vrfs list
    # this will contain all the vrfs on the device
    vrfs = []

    # set up capture vrf flag
    # this will be used to determine when to start capturing vrf name data
    # from the raw vrf command output
    capture_vrf = False

    # iterate through the raw vrf data
    for line in raw_vrf_data['stdout_lines'][0]:
        # skip empty lines
        if not line.strip():
            continue

        # set capture flag upon reaching a standard header attribute
        if 'vrf' in line.lower() and capture_vrf != True:
            capture_vrf = True
            continue

        # start capturing vrf name data
        if capture_vrf:
            # capture when these key words show up in the line
            if 'ipv4' in line or 'ipv6' in line:
                # capture vrf name
                vrf = line.split()[0]

                # add vrf name to the vrfs list
                vrfs.append(vrf)

    return vrfs

class FilterModule(object):
    """ filter module
    required class for ansible to implement custom jinja2 filters """
    
    def filters(self):
        filters = {
            'parse_nxos_vrfs': parse_nxos_vrfs,
            'parse_ios_vrfs':  parse_ios_vrfs,
            'parse_eos_vrfs': parse_eos_vrfs
        }
        return filters