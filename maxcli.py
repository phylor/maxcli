import click

from explorer import Explorer

class DeviceConfig(object):
    def __init__(self):
        self.device = None

class DiscoveryConfig(object):
    def __init__(self):
        self.broadcast_address = None

device_config = click.make_pass_decorator(DeviceConfig, ensure=True)
discovery_config = click.make_pass_decorator(DiscoveryConfig, ensure=True)

@click.group()
@click.option('--broadcast', default='192.168.1.255')
@discovery_config
def cli(config, broadcast):
    config.broadcast_address = broadcast

@cli.command()
@discovery_config
def list(config):
    devices = Explorer().discover(config.broadcast_address)

    for device in devices:
        print "{} {} {}".format(device.name, device.ip, device.sn)

@cli.group()
@click.argument('sn')
@device_config
@discovery_config
def device(config, discovery_config, sn):
    devices = Explorer().discover(discovery_config.broadcast_address)

    for device in devices:
        if device.sn == sn:
            config.device = device

@device.command()
@device_config
def status(config):
    status_info = Explorer().status(config.device)

    switch = 'On' if status_info['switch'][0] == 1 else 'Off'
    watt = status_info['watt'][0]

    click.echo('%s %s W' % (switch, watt))

@device.command()
@device_config
def on(config):
    Explorer().switch(config.device, 'on')

@device.command()
@device_config
def off(config):
    Explorer().switch(config.device, 'off')

@device.command()
@device_config
@click.argument('name', required=False)
def name(config, name):
    if name:
        Explorer().set_name(config.device, name)
    else:
        click.echo(config.device.name)
