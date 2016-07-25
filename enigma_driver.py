from enigma import enigma_machine
import configparser
import click


@click.command
# formatting options
@click.option('--spaces', type=click.Choice(['remove', 'X', 'keep']), default='remove', help='specify how to handle spaces')
@click.option('--group', default=5, help='number of characters per output grouping')
# @click.option('--verbose', is_flag=False, help='print encryption trace for each character')
# enigma setup options
@click.option('--model', type=click.STRING, default=0, help='specify enigma machine model')
@click.option('--fast', type=click.STRING, default=0, help='specify rotor id, position, and ring setting')
@click.option('--middle', type=click.STRING, default=0, help='specify rotor id, position, and ring setting')
@click.option('--slow', type=click.STRING, default=0, help='specify rotor id, position, and ring setting')
@click.option('--reflect', type=click.Choice(['UWK-A', 'UWK-B', 'UWK-C']),
              default=0, help='specify what enigma reflector to use')
@click.option('--plugs', type=click.STRING, default=0, help='specify what plugs to include on plugboard')
@click.option('--test', is_flag=False, help='run tests on all components and assemblies to ensure machine is in working order')
# config management options
@click.option('--new', type=click.STRING, help='create new user configuration')
@click.option('--delete', type=click.STRING, help='delete specified user configuration')
@click.option('--clear', is_flag=False, help='delete all user configurations')
@click.option('--lis', is_flag=False, help='list all user configurations')
@click.option('--reset', help='reset specified configuration to default configuration')
@click.option('--select', default='User', help='configuration to load')
@click.option('--once', is_flag=False, help='do not save changes to initial setup')
@click.option('--remember', is_flag=False, help='save state (position) of rotors after encryption')
# arguments
@click.argument('message', type=click.STRING)
# @click.argument('input', type=click.File('rb'))
# @click.argument('output', type=click.File('wb'))
def cli(spaces, group, model, fast, middle, slow, reflect, plugs, new, delete,
        clear, lis, reset, select, once, remember, message):

    # instantiate config parser
    config = configparser.ConfigParser(interpolation=configparser.
                                       ExtendedInterpolation())

    # check for clear
    if clear:
        for x in config.sections():
            if x != 'DEFAULT' and x != 'USER':
                config.remove_section(x)
            with open('enigma/config.ini', 'w') as configfile:
                config.write(configfile)
    # check for delete
    if delete:
        config.remove_section(delete)
        with open('enigma/config.ini', 'w') as configfile:
            config.write(configfile)
    # check for new
    if new:
        select = new
        # create new and copy options from defaults
        config[new] = {}
        for x in config.options('Default'):
            config[reset][x] = config['Default'][x]
        with open('enigma/config.ini', 'w') as configfile:
            config.write(configfile)
            # over ride will be taken care of below after setup changes are evaluated
    # check for reset
    if reset:
        config.remove_section(reset)
        config[reset] = {}
        for x in config.options('Default'):
            config[reset][x] = config['Default'][x]
        with open('enigma/config.ini', 'w') as configfile:
            config.write(configfile)
    # check for list
    if lis:
        config.read('enigma/config.ini')
        click.echo(config.sections())

    # check for setup changes
    components_to_check = {'model': model, 'fast': fast, 'middle': middle, 'slow':  slow, 'reflect': reflect, 'plug': plugs}
    components_to_change = {}
    setup_changes = False
    for key, value in components_to_check.items():
        if value != '0':
            setup_changes = True
            components_to_change[key] = value

    # is setup changes, update config files
    if setup_changes and not once:
        config.write('enigma/config.ini')
        for key, value in components_to_change.items():
            if key in ['fast', 'middle', 'slow']:
                # extract id, position, and ring setting
                if key == 'fast':
                    config[select]['r1_id'] = value[0]
                    config[select]['r1_p'] = value[1]
                    config[select]['r1_rs'] = value[2]
                if key == 'middle':
                    config[select]['r2_id'] = value[0]
                    config[select]['r2_p'] = value[1]
                    config[select]['r2_rs'] = value[2]
                if key == 'slow':
                    config[select]['r3_id'] = value[0]
                    config[select]['r3_p'] = value[1]
                    config[select]['r3_rs'] = value[2]
                else:
                    config[select][key] = value
        with open('enigma/config.ini', 'w') as configfile:
            config.write(configfile)

    # get user configurations
    config.read('enigma/config.ini')

    # load model
    enigma_model = config.getint(config, 'model')

    # load rotor ids 
    r1_id = config.getint(select, 'r1_id')
    r2_id = config.getint(select, 'r2_id')
    r3_id = config.getint(select, 'r3_id')

    # load rotor start positions
    r1_p = config.getint(select, 'r1_p')
    r2_p = config.getint(select, 'r2_p')
    r3_p = config.getint(select, 'r3_p')

    # load rotor ring settings
    r1_rs = config.getint(select, 'r1_rs')
    r2_rs = config.getint(select, 'r2_rs')
    r3_rs = config.getint(select, 'r3_rs')

    # load reflector
    ref = config.getint(config, 'reflect')

    # load plugs
    p = config.getint(config, 'plugs')

    if setup_changes and once:
        # modify appropriate components for one time use
        for key, value in components_to_change.items():
            if key in ['fast', 'middle', 'slow']:
                # extract id, position, and ring setting
                if key == 'fast':
                    r1_id = value[0]
                    r1_p = value[1]
                    r1_rs = value[2]
                if key == 'middle':
                    r2_id = value[0]
                    r2_p = value[1]
                    r2_rs = value[2]
                if key == 'slow':
                    r3_id = value[0]
                    r3_p = value[1]
                    r3_rs = value[2]
            elif key == 'model':
                enigma_model = value
            elif key == 'reflect':
                ref = value
            elif key == 'plugs':
                p = value

    # assemble rotors
    r1 = [r1_id, r1_p, r1_rs]
    r2 = [r2_id, r2_p, r2_rs]
    r3 = [r3_id, r3_p, r3_rs]
    rotors = [r1, r2, r3]

    # instantiate enigma
    e = enigma_machine.EnigmaMachine(enigma_model, rotors, ref, p)

    # todo: modify enigma_machine to report state
    # save state of machine for next use, if requested
    if remember and not once:
        pass

    # encrypt message
    ciphertext = _encrypt(e, message, spaces, group)

    # print cipher
    click.echo(ciphertext)


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
    count = 1
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
            count = (count + 1) % group
            # if not keeping spaces, group characters for readability
            if spaces.lower() != 'keep' and count == 0:
                ciphertext += " "
    return ciphertext
