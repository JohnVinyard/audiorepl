import os
import subprocess
import sys

# KLUDGE: Is there a better way to get setuptools commands?
install = 'install' in sys.argv[1:]


def run_command(cmd):
    p = subprocess.Popen(cmd, shell=True)
    rc = p.wait()
    if rc:
        # KLUDGE: What should I do here?
        raise RuntimeError()


if install:
    # make dependencies.sh executable
    run_command('chmod a+x dependencies.sh')
    # install non-python dependencies
    run_command('./dependencies.sh')

# At this point, setuptools should be available
from setuptools import setup


if install:
    run_command('pip install numpy')
    run_command('pip install cython')
    run_command('cython audiorepl/play.pyx')


def setup_jack_audio():
    # KLUDGE: This is a hack. Right?  I'd like to add the currently logged-in
    # user to the "audio" group, since JACK's installation has already setup
    # realtime audio permissions for users in that group, but the user is
    # impersonating root, so I'm using the "logname" command to guess what the
    # user's name *probably* is.

    fail_msg = 'There was a problem adding you to the audio user group : %s'

    p = subprocess.Popen( \
            'logname', shell=True, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    rc = p.wait()
    if rc:
        print fail_msg % p.stderr.read()
        return

    # the output of logname ends with a newline
    username = p.stdout.read()[:-1]
    print 'adding %s to the audio user group' % username
    # Add the current user to the audio group
    p = subprocess.Popen('usermod -a -G audio %s' % username, shell=True)
    rc = p.wait()
    if rc:
        print fail_msg % p.stderr.read()


def read(fname):
    """
    This is yanked from the setuptools documentation at
    http://packages.python.org/an_example_pypi_project/setuptools.html. It is
    used to read the text from the README file.
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


c_ext = ['*.c', '*.h']
pyx_ext = ['*.pyx', '*.pyxbld']

setup(
        name='audiorepl',
        version='0.1',
        url='http://www.johnvinyard.com',
        author='John Vinyard',
        author_email='john.vinyard@gmail.com',
        long_description=read('README.md'),
        package_data={'': c_ext + pyx_ext},
        include_package_data=True,
        packages=['audiorepl'],
        install_requires=['numpy', 'cython']
)

if install:
    setup_jack_audio()
