#! /usr/bin/env python
# -*- coding: utf-8 -*-

import bob
from bob import helper
from bob import arch
from bob import debian
from bob import config
from bob import git

import os
import sys
import optparse
import tempfile

from jinja2 import Environment, FileSystemLoader

PACKAGES = {
    'arch': arch.ArchPackage,
    'debian': debian.DebianPackage
}

class Builder(object):

    def __init__(self, target, options):

        self.config = config.Configuration()
        self.target = target
        self.options = options

        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.template_path = os.path.join(sys.prefix, 'share/bob', 'templates')
        print self.template_path
        self.package_dest = tempfile.mkdtemp(prefix='bob-')

        self.distribution = helper.guess_distribution()


    def build_package(self, package, name):

        print " » Building '{0}' for {1}".format(name, self.distribution)

        print "\n" + 40*' -' + '\n'
        status = package.build()
        print '\n' + 40*' -' + '\n'

        if status:
            print " » The build process was successful!"
            print "   → You may find the package in '{0}'…".format(status)
        else:
            print " » Build process failed!"


    def build(self):

        if self.target == 'all':
            
            for repo in self.config.repositories:
                pool = self.config.repositories[repo]['pool']
                local = os.path.join(self.config.pools[pool]['path'], repo)

                for pkg in os.listdir(local):
                    if not os.path.isfile(os.path.join(local, pkg, 'pkginfo')):
                        continue
                    pkg_src = os.path.join(local, pkg)
                    pkg_dest = os.path.join(self.package_dest, pkg)

                    jinja_env = Environment(loader=FileSystemLoader([self.template_path, pkg_dest]))

                    package = PACKAGES[self.distribution]
                    p = package(pkg_src, pkg_dest, jinja_env, self.options)

                    self.build_package(p, pkg)

                    os.chdir(self.base_path)
        else:
            pkg_src =  helper.find_package(self.target)
            pkg_dest = os.path.join(self.package_dest, self.target)

            jinja_env = Environment(loader=FileSystemLoader([self.template_path, pkg_dest]))

            package = PACKAGES[self.distribution]
            p = package(pkg_src, pkg_dest, jinja_env, self.options)

            self.build_package(p, self.target)


class Bob(object):
    
    def __init__(self):

        parser = optparse.OptionParser()
        parser.add_option('-r', '--ubuntu-release', dest='ubuntu_release', default='maverick')
        parser.add_option('-t', '--package-type', dest='package_type', default='binary')
        parser.add_option('-s', '--sync', action="store_true", dest="sync", default=False)
        options, args = parser.parse_args()
        
        self.config = config.Configuration()

        if options.sync:
            print " » Updating recipe repositories…"
            for repo in self.config.repositories:
                pool = self.config.repositories[repo]['pool']
                local = os.path.join(self.config.pools[pool]['path'], repo)
                remote = self.config.repositories[repo]['remote']
                
                if os.path.isdir(os.path.join(local, '.git')):
                    git.pull(local, remote)
                else:
                    git.clone(local, remote)
                git.checkout(local, 'master')
        else:
            print " » Not updating recipe repositories…"
        
        if not args:
            target = 'all'
        else:
            target = args[0]

        b = Builder(target, options)
        b.build()
        print " » Please remember to increase your package release numbers!"
        print " » KTHXBYE!"


if __name__ == '__main__':
    Bob()
