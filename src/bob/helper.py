import os
import re

from bob.config import Configuration

def guess_distribution():

    if os.path.isfile('/etc/lsb-release'):
        try:
            with open('/etc/lsb-release') as fd:
                release = fd.read()
                dist = re.findall('DISTRIB_ID=(?P<dist>.*)', release)[0].lower()
                if dist in ['ubuntu', 'debian']:
                    return 'debian'
                return dist
        except:
            pass

    for i in os.listdir('/etc'):
        m = re.compile('(?P<dist>.*)\-release').match(i)
        if m:
            return m.group('dist')


def find_package(package_id):

    config = Configuration()
    for repo in config.repositories:
        pool = config.repositories[repo]['pool']
        local = os.path.join(config.pools[pool]['path'], repo)
        
        if os.path.isdir(os.path.join(local, package_id)):
            return os.path.join(local, package_id)
