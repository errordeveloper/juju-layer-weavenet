from charms.reactive import when, when_not, set_state
from subprocess import check_output
from shlex import split
import os

@when('docker.available')
def install_weavenet():
    # TODO: I will find a better way to do this shortly.
    # todo - add a crypto verification
    _run("curl -sL https://git.io/weave -o /usr/local/bin/weave")
    os.chmod('/usr/local/bin/weave', 755)    
    set_state('weavenet.installed')

@when('weavenet.installed')
@when_not('weavenet.started')
def start_weave():
    _run("weave launch")
    set_state('weavenet.started') 
 

def _run(cmd):
   return check_output(split(cmd))
