#!/usr/bin/env python

import os
from distutils.core import setup
from distutils.command.install_scripts import install_scripts

class post_install(install_scripts):

    def run(self):
        install_scripts.run(self)

        from shutil import move
        for i in self.get_outputs():
            n = i.replace('.py', '')
            move(i, n)
            print "moving '{0}' to '{1}'".format(i, n)


def collect_data_files():

    data_files = []

    for directory, directories, files in os.walk('src/templates'):
        rel_dir = directory.replace('src/templates/', '')
        for file_ in files:
            data_files.append((
                'share/bob/templates',
                    [os.path.join(directory, file_)]
            ))

    return data_files


data_files = collect_data_files()
data_files.extend(
    [
    ('/etc/',
        ['src/bob.xml']),
    ])


setup(
    name = 'bob',
    version = '0.0.8',
    author = 'The Cream Project (http://cream-project.org)',
    url = 'http://github.com/cream/bob',
    data_files = data_files,
    package_dir = {'bob': 'src/bob'},
    packages = ['bob', 'bob.arch', 'bob.debian'],
    cmdclass={'install_scripts': post_install},
    scripts = ['src/bob.py']
)
