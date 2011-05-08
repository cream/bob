import bob
import bob.package
import bob.common

import subprocess
import os

class ArchPackage(bob.package.BasePackage):

    def __init__(self, src, dest, jinja_env, options):
        bob.package.BasePackage.__init__(self, src, dest, jinja_env, options)


    def build(self):

        build_dir = self.prepare_build_tree()
        self.process_template('PKGBUILD')

        p = subprocess.Popen(['makepkg', '-cfd'])
        ret = os.waitpid(p.pid, 0)[1]

        for i in os.listdir(build_dir):
            if i.endswith('.pkg.tar.xz'):
                package_path = os.path.join(build_dir, i)

        if ret != 0:
            return False
        else:
            return package_path
