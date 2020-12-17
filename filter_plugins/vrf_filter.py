class FilterModule(object):
    
    def filters(self):
        filters = {
            'parse_vrfs': self.parse_vrfs
        }
        return filters

    def parse_vrfs(self, raw_vrf_data):
        vrfs = []
        for line in raw_vrf_data['stdout_lines'][0]:
            try:
                vrf = line.split()[0].strip()
                if vrf.lower() == 'vrf-name':
                    continue
                elif vrf.lower() == 'name':
                    continue
                elif len(line.strip().split()) > 1:
                    vrfs.append(vrf)
            except:
                pass
        return vrfs