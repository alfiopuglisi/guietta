#!/usr/bin/env python
import os
import sys
from shutil import rmtree

from setuptools import setup, Command

NAME = 'guietta'
DESCRIPTION = 'Simple GUI for Python'
URL = 'https://github.com/alfiopuglisi/guietta'
EMAIL = 'alfio.puglisi@inaf.it'
AUTHOR = 'Alfio Puglisi'
LICENSE = 'MIT'
#KEYWORDS = 

# Load the package's __version__.py module as a dictionary.
here = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(here, NAME, '__version__.py')) as f:
    exec(f.read(), about)


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()


setup(name=NAME,
      description=DESCRIPTION,
      version=about['__version__'],
      classifiers=['Development Status :: 4 - Beta',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python :: 3',
                   ],
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      url=URL,
      author_email=EMAIL,
      author=AUTHOR,
      license=LICENSE,
      packages=['guietta',
                'guietta.examples',
                ],
      install_requires=['PySide2'],
      test_suite='test',
      cmdclass={'upload': UploadCommand},
      )
