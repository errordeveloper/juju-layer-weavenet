from charmhelpers.core.hookenv import leader_set, leader_get, unit_get
from charms.reactive import when, when_not, set_state, hook
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

@hook('leader-settings-changed')
def join_weave_cluster():
    ''' Followers will inherently run this hook, as the leader does not
        execute a leader-settings-changed event, it only sends data, and its
        a one way communication pipeline, like a broadcast'''
    set_state('weavenet.reconfigure')

@when('weavenet.reconfigure')
def reconfigure_weavenet():
    leader_address = leader_get('leader-address')
    _run('weave connect {}'.format(leader_address))
    remove_state('weavenet.reconfigure')



@hook('leader-elected')
def declare_weave_leader():
    ''' Only the leader knows things, so send the leadership
        address to any follower nodes so they can join in the party. 
        wake me up before you go go go '''
    leader_set('leader_address', unit_get('private-address'))

@when('weavenet.installed')
@when_not('weavenet.started')
def start_weave():
    _run("weave launch")
    set_state('weavenet.started') 
 

def _run(cmd):
   return check_output(split(cmd))
