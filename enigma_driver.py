__author__ = "Cory J. Engdahl"
__license__ = "GPL"
__version__ = "0.1.0"
__email__ = "cjengdahl@gmail.com"

from enigma import enigma_machine
import configparser
import click

# instantiate config parser
config = configparser.ConfigParser(interpolation=configparser.
                                   ExtendedInterpolation())


class DecryptAlias(click.Group):

    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        elif cmd_name == "decrypt":
            return click.Group.get_command(self, ctx, "encrypt")
        else:
            return None


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('Enigma Version %s' % __version__)
    ctx.exit()


@click.command(cls=DecryptAlias)
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)
def cli():
    pass


@cli.command()
@click.argument("configuration", type=click.STRING, required=False)
def list(configuration):
    """
    Lists the existing user configurations
    """

    config.read('enigma/config.ini')

    if configuration is not None:
        # load config
        selected = load_config(configuration)
        click.echo("Configuration %s could not be found" % configuration)

        sorted_config = []

        # convert dict to list
        for key, value in selected.items():
            sorted_config.append([key, value])
            return

        # sort
        sorted_config.sort(key=lambda x: x[0])

        for component in sorted_config:
            click.echo("%s: %s" % (component[0], component[1]))

    else:
        click.echo(config.sections())


@cli.command()
@click.option('--model', type=click.Choice(['EnigmaI', 'M2', 'M3', 'M4']), help='specify enigma machine model')
@click.option('--fast', type=click.STRING, help='specify rotor id (1-8) , position (1-26), and ring setting (1-26)'
                                                '  For example:  \'1,20,12\'')
@click.option('--middle', type=click.STRING, help='specify rotor id (1-8) , position (1-26), and ring setting (1-26)'
                                                  '  For example:  \'2,25,7\'')
@click.option('--slow', type=click.STRING, help='specify rotor id (1-8) , position (1-26), and ring setting (1-26)'
                                                '  For example:  \'5,21,19\'')
@click.option('--static', type=click.STRING, help='specify rotor id (9 for beta, 10 for gamma), position (1-26), '
                                                  'and ring setting (1-26)    For example:\'1,20,12\'')
@click.option('--reflect', type=click.Choice(['UWK-A', 'UWK-B', 'UWK-C']), help='specify what enigma reflector to use')
@click.option('--plugs', type=click.STRING, help='specify what plugs to include on plugboard'
                                                 '  For example: \'AB,DY,UI,QK\'')
@click.argument('new', type=click.STRING, required=True)
def new(new, model, fast, middle, slow, static, reflect, plugs):
    """
    Creates and saves new user configuration for enigma machine.  New configuration is based on default configuration
    overwritten with invoked options.
    """

    # load default
    local_config = load_config('User')

    # add changes locally
    options = {'model': model, 'fast': fast, 'middle': middle, 'slow':  slow, 'static': static, 'reflect': reflect, 'plugs': plugs}
    local_config = update_config(local_config, options)

    # assembly enigma machine
    # todo: handle exceptions
    enigma = assemble_enigma(local_config)

    # create new config and write local configuration to it
    config[new] = {}
    write_config(new, local_config)


@cli.command()
def clear():
    """
    Clears all users configurations except 'Default' and 'User'
    """

    config.read('enigma/config.ini')

    for x in config.sections():
        if x.upper() not in ['DEFAULT', 'USER']:
            config.remove_section(x)
        with open('enigma/config.ini', 'w') as configfile:
            config.write(configfile)


@cli.command()
@click.argument('delete', type=click.STRING, required=True)
def delete(delete):
    """
    Deletes specified user configurations. Default and User configs
    can not be deleted
    :param delete:
    :return:
    """

    config.read('enigma/config.ini')

    if delete.upper() not in ['DEFAULT', 'USER']:

        # gather all configurations
        configurations = []
        for x in config.sections():
            configurations.append(x.upper())

        if delete.upper() not in configurations:
            click.echo("Error: configuration \"%s\" does not exist, cannot delete" %delete)

        else:
            config.remove_section(delete)
            with open('enigma/config.ini', 'w') as configfile:
                config.write(configfile)
    else:
        click.echo("Error: Cannot delete \"Default\" and \"User\" configurations")


@cli.command()
@click.argument('reset', type=click.STRING, required=True)
def reset(reset):
    """
    Resets specified configuration to \"Default\" settings
    :param reset:
    :return:
    """

    config.read('enigma/config.ini')

    if reset.upper() != 'DEFAULT':
        # gather all configurations
        configurations = []
        for x in config.sections():
            configurations.append(x.upper())

        if reset.upper() not in configurations:
            click.echo("Error: configuration \"%s\" does not exist, cannot reset" % reset)

        else:
            config.remove_section(reset)
            config[reset] = {}
            for x in config.options('Default'):
                config[reset][x] = config['Default'][x]
            with open('enigma/config.ini', 'w') as configfile:
                config.write(configfile)

    else:
        click.echo("Error: Cannot reset \"Default\" configuration")



@cli.command()
# formatting options
@click.option('--spaces', '-s', type=click.Choice(['remove', 'X', 'keep']), default='remove', help='specify how to handle spaces')
@click.option('--group', '-g', default=5, help='number of characters per output grouping')
# enigma setting options
@click.option('--model', type=click.STRING, help='specify enigma machine model')
@click.option('--fast', '-r1', type=click.STRING, help='specify rotor id, position, and ring setting')
@click.option('--middle', '-r2', type=click.STRING, help='specify rotor id, position, and ring setting')
@click.option('--slow', '-r3', type=click.STRING, help='specify rotor id, position, and ring setting')
@click.option('--static', '-r4', type=click.STRING, help='specify rotor id, position, and ring setting.'
                                                  '(only applicable for M4 mode)')
@click.option('--reflect', type=click.Choice(['UKW-A', 'UKW-B', 'UKW-C']), help='specify what enigma reflector to use')
@click.option('--plugs', type=click.STRING, help='specify what plugs to include on plugboard')
# config management options
@click.option('--select', default='User', help='configuration to load')
@click.option('--once', is_flag=True, help='do not save changes to initial setup')
@click.option('--remember', is_flag=True, help='save state (position) of rotors after encryption')
# input/output options
@click.option('--input', '-f', type=click.File('r'), required=False)
@click.option('--output', '-o', type=click.File('w'), required=False)
# arguments
@click.argument('message', type=click.STRING, required=False)
def encrypt(spaces, group, model, fast, middle, slow, static, reflect, plugs, select, once, remember, message, input, output):
    """
    Command Line Interface tool for Enigma Machine
    """

    # get user configurations
    config.read('enigma/config.ini')

    # load model
    local_config = load_config(select)

    # add changes locally
    options = {'model': model, 'fast': fast, 'middle': middle, 'slow':  slow, 'static': static, 'reflect': reflect, 'plugs': plugs}
    local_config = update_config(local_config, options)

    # assembly enigma machine
    # todo: handle exceptions
    enigma = assemble_enigma(local_config)

    # if enigma assembled without error, write config
    if not once:
        write_config(select, local_config)

    # todo: modify enigma_machine to report state
    # save state of machine for next use, if requested
    if remember and not once:
        pass

    if message is None and input is not None:
            message = input.read().replace('\n', '')

    # encrypt message
    ciphertext = _encrypt(enigma, message, spaces, group)

    # print cipher
    if output is not None:
        output.write(ciphertext)

    else:
        click.echo(ciphertext)


##################################
#      Local Helper Methods      #
##################################


def _encrypt(enigma, message, spaces, group):
    """
    Encrypts input and directs output appropriately, with standard-out as
    the default. It also controls output format.  By default, characters
    are encrypted in groups of 5.  If spaces are not previously filtered out,
    output will not group characters but instead encrypt with spacing in its
    natural state.  All input must be upper case, or it will not be encrypted.
    :return:
    """

    plaintext = message.upper()
    ciphertext = ""
    count = 0
    for c in plaintext:

        # if character is a space
        if ord(c) == 32:

            # and option is set to remove
            if spaces.lower() == 'remove':
                # do nothing (will not be entered into enigma)
                pass

            # and option is set to 'X
            elif spaces.lower() == 'x':
                # replace the space with the character 'X' and encrypt
                ciphertext += enigma.encrypt('X')

            # otherwise, the space will be evident in the cipher text
            else:
                ciphertext += " "

        # if character is illegal, remove it
        elif ord(c) < 65 or ord(c) > 90:
            # do nothing (will not be entered into enigma)
            pass

        # otherwise character is legal, encrypt it
        else:
            ciphertext += enigma.encrypt(c)
            if group != 0:
                count = (count + 1) % group
                # if not keeping spaces, group characters for readability
                if spaces.lower() != 'keep' and count == 0:
                    ciphertext += " "
    return ciphertext

def update_config(local_config, changes):
    """
    Updates local config dict with changes from cli invoked options
    :param local_config (dict): loaded enigma configuration where key = component, value = setting
    :param changes (dict) : changes to be made to loaded configuration, where key = component, value = desired setting
    :return (dict): loaded configuration with new changes from invoked cli options
    """

    for key, value in changes.items():
        if value is not None:
            if key == 'fast':
                rotor = [int(x) for x in value.split(",")]
                local_config['r1_id'] = rotor[0]
                local_config['r1_p'] = rotor[1]
                local_config['r1_rs'] = rotor[2]
            elif key == 'middle':
                rotor = [int(x) for x in value.split(",")]
                local_config['r2_id'] = rotor[0]
                local_config['r2_p'] = rotor[1]
                local_config['r2_rs'] = rotor[2]
            elif key == 'slow':
                rotor = [int(x) for x in value.split(",")]
                local_config['r3_id'] = rotor[0]
                local_config['r3_p'] = rotor[1]
                local_config['r3_rs'] = rotor[2]
            elif key == 'static':
                rotor = [int(x) for x in value.split(",")]
                local_config['r4_id'] = rotor[0]
                local_config['r4_p'] = rotor[1]
                local_config['r4_rs'] = rotor[2]
            elif key == 'plugs':
                plugs = value.split(",")
                local_config['plugs'] = plugs
            else:
                local_config[key] = value

    return local_config

def load_config(config_name):
    """
    Loads the options and values of an existing configurations into a dictionary
    :param config_name (str): name of configuration to change
    :return (dict/bool) : dictionary of components
    """

    config.read('enigma/config.ini')

    # # todo: check if config exists
    # if not config_name in config:
    #     # indicate error and close program
    #     click.echo("%s is not a valid configuration" %config_name)
        
    components = {}

    # load all components and convert rotor parameters to integer
    for x in config.options(config_name):
        if x in ['r1_id', 'r2_id', 'r3_id', 'r4_id', 'r1_p', 'r2_p', 'r3_p', 'r4_p',
                                      'r1_rs', 'r2_rs', 'r3_rs', 'r4_rs']:
            value = int(config[config_name][x])
        elif x == 'plugs':
            value = config[config_name][x].split(",")

        else:

            value = config[config_name][x]

        components[x] = value

    return components

def write_config(config_name, local_config):
    """
    Writes locally stored config file to to initiailizeation (.ini) file
    :param config_name (str): name of config section to write (i.e. name of configuration)
    :param local_config (dic) : dict of locally stored enigma configuration
    :return:
    """

    sorted_config = []

    # convert dict to list
    for key, value in local_config.items():
        sorted_config.append([key, value])

    #sort
    sorted_config.sort(key=lambda x: x[0])

    for component in sorted_config:
        if component[0] == 'plugs':
            plugs = ""
            for plug in component[1]:
                plugs += plug + ","
            config[config_name][component[0]] = plugs[:len(plugs)-1]

        else:
            config[config_name][component[0]] = str(component[1])

    # write the changes
    with open('enigma/config.ini', 'w') as configfile:

        config.write(configfile)


def assemble_enigma(components):
    """
    Assembles enigma machine from local config dict
    :param components (dict): local config file.  key = component, value = setting
    :return (enimga_machine):
    """
    # assemble rotors from config file
    r1 = [components['r1_id'], components['r1_p'], components['r1_rs']]
    r2 = [components['r2_id'], components['r2_p'], components['r2_rs']]
    r3 = [components['r3_id'], components['r3_p'], components['r3_rs']]
    if components['model'] == 'M4':
        r4 = [components['r4_id'], components['r4_p'], components['r4_rs']]
        rotors = [r1, r2, r3, r4]

    else:
        rotors = [r1, r2, r3]

    # assemble enigma from config file
    e = enigma_machine.EnigmaMachine(components['model'], rotors, components['reflect'], components['plugs'])

    return e



