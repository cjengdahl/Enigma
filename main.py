import configparser
import enigma.py


config =configparser.ConfigParser(interpolation= configparser.ExtendedInterpolation())


def main():

    #load model
    config.read('config.ini')
    user_config = {}

    user_config['model'] = ConfigSectionMap('User', 'model', 'configString')
    user_config['num_plugs'] = ConfigSectionMap('User', 'num_plugs', 'configInt')
    user_config['uhr'] = ConfigSectionMap('User', 'uhr', 'configBool')
    user_config['schreibmax'] = ConfigSectionMap('User', 'schreibmax', 'configBool')
    user_config['lock_1'] = ConfigSectionMap('User', 'lock_1',	'configBool')
    user_config['lock_2'] = ConfigSectionMap('User', 'lock_2', 'configBool')
    user_config['lamp_mode'] = ConfigSectionMap('User', 'lamp_mode', 'configBool')
    user_config['printer_address'] = ConfigSectionMap('User', 'printer_address', 'configString')
    user_config['trace'] = ConfigSectionMap('User', 'trace', 'configBool')
    user_config['input_file'] = ConfigSectionMap('User', 'input_file', 'configString')
    user_config['output_file'] = ConfigSectionMap('User', 'output_file', 'configString')

    #load model configuration
    config.read('model.ini')
    model = user_config['model']
    model_config = {}
	
    model_config['max_rotors'] = ConfigSectionMap(model, 'max_rotors', 'configInt')
    model_config['max_plugs'] = ConfigSectionMap(model, 'max_plugs', 'configInt')
    model_config['rotors'] = ConfigSectionMap(model, 'rotors', 'configList')
    model_config['reflectors'] = ConfigSectionMap(model, 'reflectors', 'configList')
    model_config['locks'] = ConfigSectionMap(model, 'locks', 'configBool')
    model_config['r_numeric'] = ConfigSectionMap(model, 'r_numeric', 'configBool')
    model_config['r_alpha'] = ConfigSectionMap(model, 'r_alpha', 'configBool')
    model_config['p_numeric'] = ConfigSectionMap(model, 'p_numeric', 'configBool')
    model_config['p_alpha'] = ConfigSectionMap(model, 'p_alpha', 'configBool')
    model_config['uhr'] = ConfigSectionMap(model, 'uhr', 'configBool')
    model_config['schreibmax'] = ConfigSectionMap(model, 'schreibmax', 'configBool')

    # cross check user config with model constraints
    if user_config['num_plugs']	> model_config['max_plugs']:
        print("invalid number of plugs")
        # Error, too many plugs in use

    if user_config['uhr']:
        print("uhr on")
        # use uhr as an additional component

    if user_config['schreibmax']:
        print("printer enable")
        # print output file to defined printer
        # user_config['printer_address']

    if user_config['lock_1']:
        if model_config['locks'] > 0:
            # lock no allowed
            print("Lock 1 Enabled")

    if user_config['lock_2']:
        if model_config['locks'] > 1:
            # lock no allowed	
            print("Lock 1 Enabled")

    # if user_config['input_file']
    # read from input file

    # if user_config['output_file']
    # write to output file

    if user_config['lamp_mode']:
        # display only encrypted letter when key is pressed
        print("lamp mode on")

    if user_config['trace']:
        # show encryption path per letter
        print("trace enable")

    # create enigma(s)

    # encrypt


def ConfigSectionMap(section, option, opType):
    options = config.options(section)

    # cast boolean
    if opType == "configBool":
        try:
            value = config.getboolean(section, option)
            if value == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            value = None

    # cast integer
    elif opType == "configInt":
        try:
            value = config.getint(section, option)
            if value == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            value = None

    # cast list (of strings)
    elif opType == "configList":
        try:
            value = config.get(section, option)
            if value == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            value = None

    # value = list(value)		

    # no cast (read as string)
    else:
        try:
            value = config.get(section, option)
            if value == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            value = None

    # create enigma machine
    enigma = enigma()
    
    return value


if __name__ == '__main__':
    main()
