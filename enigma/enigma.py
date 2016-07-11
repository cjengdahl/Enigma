import enigma_machine
import click


@click.command()
@click.option('--spaces', type=click.Choice(['remove', 'X', 'keep']))
@click.option('--group', default=5)
# @click.argument('input', type=click.File('rb'))
# @click.argument('output', type=click.File('wb'))
def cli(message, spaces, group):
    fast = [5, 4, 21]
    middle = [2, 19, 8]
    slow = [4, 13, 2]
    rot = [fast, middle, slow]
    ref = "UKW-A"
    plugs = ["AK", "BC", "UD", "PI", "QX"]
    e = enigma_machine.EnigmaMachine("ENIGMAI", rot, ref, plugs)

    plaintext = filter(message, spaces)
    ciphertext = encrypt(e, plaintext, spaces, group)
    click.echo(ciphertext)


def filter(message, spaces):
    """
    Modifies input comply with the capabilities of the enigma machine.
    This includes: case adjustment, space removal, space replacement,
    and illegal character removal
    :param message:
    :param group:
    :param spaces:
    :param ill:
    :return:
    """
    message = message.upper
    plaintext = ""

    for c in message:

        # if character is a space
        if ord(c) == 32:

            # and option is set to remove
            if spaces.lower() == 'remove':
                # do nothing to remove(will not be entered into enigma)
                pass

            # and option is set to 'X
            elif spaces.lower() == 'x':
                # replace the space with the character 'X'
                plaintext += 'X'

            # otherwise, the space will be evident in the cipher text

        # if character is illegal, remove it
        elif ord(c) < 65 or ord(c) > 90:
            # do nothing to remove (will not be entered into enigma)
            pass

        # valid character
        else:
            plaintext += c

    return plaintext


def encrypt(enigma, message, spaces, group):
    """
    Encrypts input and directs output appropriately, with standard-out as
    the default. It also controls output format.  By default, characters
    are encrypted in groups of 5.  If spaces are not previously filtered out,
    output will not group characters but instead encrypt with spacing in its
    natural state.  All input must be upper case, or it will not be encrypted.
    :return:
    """
    # short form spaces
    keep_spaces = spaces.lower == "keep"

    ciphertext = ""
    count = 1
    for c in message:
        if (keep_spaces and ord(c) == 32) or count:
            ciphertext += " "
        else:
            ciphertext += enigma.encrypt(c)
            count += 1 % group
            # if not keeping spaces, group characters for readability
            if not keep_spaces and count == 0:
                ciphertext += " "

    return ciphertext


@click.command()
def configure(model='ENIGMAI', rotorIds="123", rotorPos="111",
              rotorRings='111', reflect='UKW-B', plugs=""):
    """
    Configures enimga machine to indicated states
    :param model:
    :param rotorIds:
    :param rotorPos:
    :param rotorRings:
    :param reflect:
    :param plugs:
    :return:
    """

    pass
