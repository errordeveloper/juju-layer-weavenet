from charms.reactive import when, when_not, set_state

@when('docker.available')
@when_not('weavenet.installed')
def install_weavenet():
    pass
    set_state('weavenet.installed')
