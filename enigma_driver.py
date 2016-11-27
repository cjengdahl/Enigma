__author__ = "Cory J. Engdahl"
__license__ = "MIT"
__version__ = "0.1.0"
__email__ = "cjengdahl@gmail.com"

from enigma import enigma_machine
from enigma import enigma_exception
import configparser
import click
import os

# instantiate config parser
config = configparser.ConfigParser(interpolation=configparser.
                                   ExtendedInterpolation())

pwd = os.path.dirname(__file__)
user_configs = os.path.join(pwd, 'config/config.ini')


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

    if len(config.read(user_configs)) == 0:
        click.echo("\nConfig file, \"config.ini\", not found\n")
        return

    if configuration is not None:
        # load config
        try:
            selected = load_config(configuration)

        except configparser.NoSectionError:
            click.echo("Configuration %s could not be found" % configuration)
            return

        sorted_config = []

        # convert dict to list
        for key, value in selected.items():
            sorted_config.append([key, value])

        # sort
        sorted_config.sort(key=lambda x: x[0])

        click.echo("\n%s:\n" % configuration)
        for component in sorted_config:
            click.echo("%s: %s" % (component[0], component[1]))
        click.echo("\n")

    else:
        click.echo("\nAvailable Configurations:\n")
        sections = config.sections()
        for section in sections:
            # preferences is not a config
            if section.upper() != 'PREFERENCES':
                click.echo(section)
        click.echo("\n")


@cli.command()
@click.option('--spaces', type=click.Choice(['remove', 'X', 'keep']), help='set default space handling preference')
@click.option('--space-detect', '-d', type=click.Choice(['True', 'False']), help='enable space detection, decrypted Xs are converted to spaces.')
@click.option('--group', type=click.STRING, help='set default letter grouping preference')
@click.option('--remember', type=click.Choice(['True', 'False']),
              help='set enigma machine to remember machine state after encryption')
def pref(spaces, group, remember, space_detect):
    """
    Lists the default preferences.  Invoked options updates preferences
    """

    if len(config.read(user_configs)) == 0:
        click.echo("\nConfig file, \"config.ini\", not found\n")
        return

    options = ['spaces', 'group', 'remember', 'space_detect']
    updated_options = {}
    for option in options:
        if eval(option) is not None:              
            updated_options[option] = eval(option)

    if len(updated_options) != 0:
        # update preferences
        write_config("Preferences", updated_options)
        click.echo("\nPreferences updated\n")

    # list all preferences
    else:
        try:
            selected = load_config("Preferences")

        except configparser.NoSectionError:
            click.echo("Preferences could not be found")
            return

        preferences = []

        # convert dict to list
        for key, value in selected.items():
            preferences.append([key, value])

        # sort
        preferences.sort(key=lambda x: x[0])

        click.echo("\nPreferences:\n")
        for pref in preferences:
            click.echo("%s: %s" % (pref[0], pref[1]))
        click.echo("\n")

        return


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
@click.option('--reflect', type=click.Choice(['UKW-A', 'UKW-B', 'UKW-C', 'UKW-B_THIN', 'UKW-C_THIN']),
              help='specify what enigma reflector to use')
@click.option('--plugs', type=click.STRING, help='specify what plugs to include on plugboard'
                                                 '  For example: \'AB,DY,UI,QK\'')
@click.argument('configuration', type=click.STRING, required=True)
def new(configuration, model, fast, middle, slow, static, reflect, plugs):
    """
    Creates and saves new user configuration for enigma machine.  New configuration is based on default configuration
    overwritten with invoked options.
    """

    if model == "M4" and (static is None or reflect is None):
        click.echo("Cannot create configuration, M4 model requires static rotor and thin reflector")
        return

    # load default
    local_config = load_config('Default')

    # add changes locally
    options = {'model': model, 'fast': fast, 'middle': middle, 'slow':  slow, 'static': static, 'reflect': reflect,
               'plugs': plugs}
    local_config = update_config(local_config, options)

    # assembly enigma machine
    try:
        enigma = assemble_enigma(local_config)

    except enigma_exception.DuplicatePlug:
        click.echo("Cannot create configuration, duplicate plugs are not allowed")
        return
    except enigma_exception.MaxPlugsReached:
        click.echo("Cannot create configuration.  More plugs than allowed have been specified")
        return
    except enigma_exception.DuplicateRotor:
        click.echo("Cannot create configuration, duplicate rotors are not allowed")
        return
    except enigma_exception.InvalidRotor:
        click.echo("Cannot create configuration, invalid rotor specified")
        return
    except enigma_exception.InvalidRotorFour:
        click.echo("Cannot create configuration, invalid static rotor specified.  "
                   "Must use rotor id 9 (Beta) or 10 (Gamma)")
        return
    except enigma_exception.InvalidReflector:
        click.echo("Cannot create configuration, invalid reflector specified")
        return

    # create new config and write local configuration to it
    config[configuration] = {}
    write_config(configuration, local_config)


@cli.command()
def clear():
    """

    Clears all users configurations except 'Default' and 'User'
    """

    config.read(user_configs)

    for x in config.sections():
        if x.upper() not in ['DEFAULT', 'USER', 'PREFERENCES']:
            config.remove_section(x)

    # set config preference to User
    config["Preferences"]["config"] = "User"

    with open(user_configs, 'w') as configfile:
            config.write(configfile)


@cli.command()
@click.argument('configuration', type=click.STRING, required=True)
def delete(configuration):
    """
    Deletes specified user configurations. Default and User configs
    can not be deleted
    """

    if len(config.read(user_configs)) == 0:
        click.echo("\nConfig file, \"config.ini\", not found\n")
        return

    if configuration.upper() not in ['DEFAULT', 'USER']:

        if configuration.upper() == "PREFERENCES":
            click.echo("\nConfiguration \"%s\" does not exist, cannot delete\n" % configuration)
            return

        # gather all configurations
        configurations = []
        sections = config.sections()
        
        if len(sections) == 3:
            click.echo("\nConfiguration file contains no delete-able configurations\n")
            return

        for x in sections:
            configurations.append(x)

        if configuration not in configurations:
            click.echo("Configuration \"%s\" does not exist, cannot delete" % configuration)

        else:
            # remove config
            config.remove_section(configuration)

            # if config to be deleted is config preference
            if config["Preferences"]["config"] == configuration:
                # update config preference to be User config
                config["Preferences"]["config"] = "User"

            with open('user_configs', 'w') as configfile:
                config.write(configfile)
    else:
        click.echo("\nCannot delete \"Default\" or \"User\" configurations\n")


@cli.command()
@click.argument('configuration', type=click.STRING, required=True)
def reset(configuration):
    """
    Resets specified configuration to \"Default\" settings
    """

    if len(config.read(user_configs)) == 0:
        click.echo("\nConfig file, \"config.ini\", not found\n")
        return

    if configuration.upper() != 'DEFAULT':
        # gather all configurations
        configurations = []
        sections = config.sections()
        
        if len(sections) == 0:
            click.echo("\nConfiguration file contains no configurations\n")
            return

        for x in sections:
            configurations.append(x.upper())

        if (configuration.upper() not in configurations) or configuration.upper() == "PREFERENCES":
            click.echo("\nconfiguration \"%s\" does not exist, cannot reset\n" % configuration)

        else:
            config.remove_section(configuration)
            config[configuration] = {}
            for x in config.options('Default'):
                config[configuration][x] = config['Default'][x]
            with open(user_configs, 'w') as configfile:
                config.write(configfile)

    else:
        click.echo("\nCannot reset \"Default\" configuration\n")


@cli.command()
# formatting options
@click.option('--spaces', '-s', type=click.Choice(['remove', 'X', 'keep']), help='specify how to handle spaces')
@click.option('--space-detect', '-d', type=click.Choice(['True', 'False']), help='enable space detection, decrypted Xs are converted to spaces.')
@click.option('--group', '-g', help='number of characters per output grouping')
# enigma setting options
@click.option('--model', type=click.STRING, help='specify enigma machine model')
@click.option('--fast', '-r1', type=click.STRING, help='specify rotor id, position, and ring setting')
@click.option('--middle', '-r2', type=click.STRING, help='specify rotor id, position, and ring setting')
@click.option('--slow', '-r3', type=click.STRING, help='specify rotor id, position, and ring setting')
@click.option('--static', '-r4', type=click.STRING, help='specify rotor id, position, and ring setting.'
              '(only applicable for M4 mode)')
@click.option('--reflect', type=click.Choice(['UKW-A', 'UKW-B', 'UKW-C', 'UKW-B_THIN', 'UKW-C_THIN']),
              help='specify what enigma reflector to use')
@click.option('--plugs', type=click.STRING, help='specify what plugs to include on plugboard')
# config management options
@click.option('--select', help='configuration to load')
@click.option('--update', '-u', is_flag=True, help='overwrite config file with invoked preference and component option')
@click.option('--remember', type=click.Choice(['True', 'False']), help='save state (position) of rotors after encryption')
# input/output options
@click.option('--input', '-f', type=click.File('r'), required=False)
@click.option('--output', '-o', type=click.File('w'), required=False)
# arguments
@click.argument('message', type=click.STRING, required=False)
def encrypt(spaces, group, model, fast, middle, slow, static, reflect, plugs, select, update, remember, message,
            input, output, space_detect):
    """
    Command Line Interface tool for Enigma Machine
    """

    # get user configurations
    if len(config.read(user_configs)) == 0:
        click.echo("\nConfig file, \"config.ini\", not found\n")
        return

    # load preferences
    try:
        preferences = load_config("Preferences")

    except configparser.NoSectionError:
        click.echo("Preferences could not be found" % select)
        return

    # load model
    try:

        if select is None:
            # load config in preferences
            select = preferences["config"]

        local_config = load_config(select)

    except configparser.NoSectionError:
        click.echo("Configuration %s could not be found" % select)
        return

    # add config changes locally
    options = {'model': model, 'fast': fast, 'middle': middle, 'slow':  slow, 'static': static, 'reflect': reflect,
               'plugs': plugs}

    local_config = update_config(local_config, options)

    # add preferences locally
    pref_options = {'spaces': spaces, 'group': group, 'remember': remember,
                    'config': select, 'space_detect': space_detect}

    preferences = update_config(preferences, pref_options)

    # assembly enigma machine
    try:
        enigma = assemble_enigma(local_config)

    except enigma_exception.DuplicatePlug:
        click.echo("Cannot create configuration, duplicate plugs are not allowed")
        return
    except enigma_exception.MaxPlugsReached:
        click.echo("Cannot create configuration.  More plugs than allowed have been specified")
        return
    except enigma_exception.DuplicateRotor:
        click.echo("Cannot create configuration, duplicate rotors are not allowed")
        return
    except enigma_exception.InvalidRotor:
        click.echo("Cannot create configuration, invalid rotor specified")
        return
    except enigma_exception.InvalidRotorFour:
        click.echo("Cannot create configuration, invalid static rotor specified")
        return
    except enigma_exception.InvalidReflector:
        click.echo("Cannot create configuration, invalid reflector specified, check model compatibility")
        return

    # if enigma assembled without error and update is specified, write config and preferences to config file
    if update:
        write_config(select, local_config)
        write_config("Preferences", preferences)

    # match preference options to local preferences
    spaces = preferences["spaces"]

    group = int(preferences["group"])
    remember = preferences["remember"]
    space_detect = preferences["space_detect"]  

    # ensure type
    space_detect = str_to_bool(space_detect)

    if message is None and input is not None:
            message = input.read().replace('\n', ' ')

    # encrypt message
    ciphertext = _encrypt(enigma, message, spaces, space_detect, group)

    # todo: modify enigma_machine to report state
    # save state of machine for next use, if requested
    if str_to_bool(remember):

        # get position of rotors 1-3 and write to config file
        r1_p = enigma.rotor_pos("r1")
        r2_p = enigma.rotor_pos("r2")
        r3_p = enigma.rotor_pos("r3")

        # replace value in config file
        config[select]["r1_p"] = str(r1_p)
        config[select]["r2_p"] = str(r2_p)
        config[select]["r3_p"] = str(r3_p)

        # write changes
        with open(user_configs, 'w') as configfile:
            config.write(configfile)

    # print cipher
    if output is not None:
        output.write(ciphertext)

    else:
        click.echo(ciphertext)


##################################
#      Local Helper Methods      #
##################################


def _encrypt(enigma, message, spaces, space_detect, group):
    """
    Encrypts input and directs output appropriately, with standard-out as
    the default. It also controls output format.  By default, characters
    are encrypted in groups of 5.  If spaces are not previously filtered out,
    output will not group characters but instead encrypt with spacing in its
    natural state.  All input must be upper case, or it will not be encrypted.
    :return:
    """

    # todo:  notification of some sort....

    # if space_detect, remove all spaces for processing
    if space_detect:
        spaces = "remove"
        group = 0

    if message is None:
        return

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
            e = enigma.encrypt(c)
            # if space detect enabled, replaces Xs with spaces
            if space_detect and e == 'X':
                ciphertext += " "
            else:
                ciphertext += e
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

    config.read(user_configs)
        
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
    Writes locally stored config file to to initialization (.ini) file
    :param config_name (str): name of config section to write (i.e. name of configuration)
    :param local_config (dic) : dict of locally stored enigma configuration
    :return:
    """

    sorted_config = []

    # convert dict to list
    for key, value in local_config.items():
        sorted_config.append([key, value])

    # sort
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
    with open(user_configs, 'w') as configfile:

        config.write(configfile)


def assemble_enigma(components):
    """
    Assembles enigma machine from local config dict
    :param components (dict): local config file.  key = component, value = setting
    :return (enigma_machine):
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


def str_to_bool(string):
    """
    Converts strings to boolean
    :param string (str): string to convert
    : retrun (bool): True if string is equal to "True", False if equal to "False"
    """

    if string == "True":
        return True
    elif string == "False":
        return False
    else:
        return string
