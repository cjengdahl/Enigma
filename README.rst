==========
enigma-cli
==========

:Author: Cory J. Engdahl
:Email: cjengdahl@gmail.com
:Webpage:  http://www.cjengdahl.com
:License: MIT


Description
------------

German Enigma Machine Command-Line Tool (EnigmaI, M1, M2, M3, M4 Models).
Replicates the exact functionality of the physical machines used in WWII
with an easy to use command-line interface.


Installation
------------

enigma requires the installation of the python3_ interpreter.  The only third-party package dependency is Click_.  If you choose to install via pip, Click will be installed as well.

.. _python3: https://www.python.org/download/releases/3.0/
.. _Click: http://click.pocoo.org

|  **Install with pip:**

|  ``pip install enigma-cli``

The source can be cloned from https://github.com/cjengdahl/Enigma

Configuration
-------------

Just like an actual Enigma Machine, the simulated machine must be configured before use.  The configuration 
serves as the 'key'.  The same key is used to encrypt and decrypt text. The setup configurations are stored in a config file, which can be modified through the command line interface.  A default configuration is always available, along with a single, modifiable user configuration named 'User'.  It is required
that the following items are specified before use:

| * Enigma Model
| * Rotors Used (ID)
| * Rotor Start Postions
| * Rotor Ring Postions 
| * Reflector
| * Plugs Inserted In Plugboard


Preferences
-----------

In addition to the machine configuration, there are also user preferences that can be set. These include output grouping, newline removal, space handling, space detection, default configuration, and state remembrance.

| * **Output grouping** groups the output text to the specified number of characters.  Historically, messages where separated by a space every five characters.  This preference is ignored if the space handling preference is set to 'keep'.

| * **Newline removal** replaces newline characters with a space.  This is only applicable to file input, not encrypting directly from standard input.  

| * **Space handling** allows the user to specify if spaces should be kept in the cipher text, removed, or replaced with an "X" before encryption.  Historically, it was common to replace spaces with an "X" because the character itself was not commonly used.  

| * **Space detection** goes hand in hand with the space replacement.  During the decryption process, if an "X" is found, it is replaced with a space. 

| * The **default configuration** is the configuration that will be loaded automatically every time an enigma command is executed.  By default, the "User" configuration is loaded; however, addition configurations can be specified.

| * Lastly, the enigma can be placed in a **state of remembrance**.  With this enabled, for each character encrypted/decrypted the state of the machine is saved the nexted use (i.e. the rotor positions are saved after use)


Usage
-----

enigma [OPTIONS] COMMAND [ARGS]...

Commands are listed as follows:


encrypt <text>
~~~~~~~~~~~~~~

Encrypts text input with Enigma Machine.  All input is converted to uppercase and non-alphabetic characters (with the exception of spaces and newline characters) are removed.  Text is optional and takes priority over file input.

**Alias:**  decrypt

**Options:**

    ===================================================================     ==========================================================================================

    ``-s, --spaces [remove | X | keep]``                                     Set space handling preference

    ``-n, --newlines [True | False]``                                        Include newline characters

    ``-d, --space-detect [True | False]``                                    Convert decrypted Xs to spaces

    ``-g, --group TEXT``                                                     Set output letter grouping

    ``-m, --model TEXT``                                                     Enigma machine model

    ``-r1, --fast TEXT``                                                     Fast rotor config: id (1-8) , position (1-26), and ring setting (1-26)

    ``-r2, --middle TEXT``                                                   Middle rotor config: id (1-8) , position (1-26), and ring setting (1-26)

    ``-r3, --slow TEXT``                                                     Slow rotor config: id (1-8) , position (1-26), and ring setting (1-26)

    ``-r4, --static TEXT``                                                   Static rotor config: (9 for beta, 10 for gamma), position (1-26), and ring setting (1-26)

    ``-r, --reflect [UKW-A | UKW-B | UKW-C | UKW-B_THIN | UKW-C_THIN]``      Enigma reflector

    ``-p, --plugs TEXT``                                                     Plugs inserted in plugboard (e.g. "AB,XY")

    ``-c, --select TEXT``                                                    Select enigma machine configuration

    ``-u, --update``                                                         Overwrite config file with invoked preferences, and options

    ``-k, --remember [True | False]``                                        Remember machine state after encryption

    ``-f, --input FILENAME``                                                 Path to input file

    ``-o, --output FILENAME``                                                Path to output file

    ===================================================================     ==========================================================================================

clear
~~~~~

Clears all users configurations with the exception of 'Default' and 'User'.

delete <configuration>
~~~~~~~~~~~~~~~~~~~~~~

Deletes specified user configuration. Default and User configs can not be deleted

list <configuration>
~~~~~~~~~~~~~~~~~~~~

Lists the existing user configurations.  Lists configuration details if specific configuration provided as an argument

new <configuration>
~~~~~~~~~~~~~~~~~~~

**Options:**

    ===================================================================         =========================================================================================                                   

    ``-m, --model [EnigmaI | M2 | M3 | M4]``                                    Enigma machine model

    ``-r1, --fast TEXT``                                                        Fast rotor config: id (1-8) , position (1-26), and ring setting (1-26)

    ``-r2, --middle TEXT``                                                      Middle rotor config: id (1-8) , position (1-26), and ring setting (1-26)

    ``-r3, --slow TEXT``                                                        Slow rotor config: id (1-8) , position (1-26), and ring setting (1-26)

    ``-r4, --static TEXT``                                                      Static rotor config: (9 for beta, 10 for gamma), position (1-26), and ring setting (1-26)

    ``-r, --reflect [UKW-A | UKW-B | UKW-C | UKW-B_THIN | UKW-C_THIN]``         Enigma reflector

    ``-p, --plugs TEXT``                                                        Plugs inserted in plugboard (e.g. "AB,XY")

    ===================================================================         =========================================================================================                                      

pref
~~~~ 

Manages the default preferences.  Invoked options updates preferences

**Options:**

    =====================================     ========================================

    ``-s, --spaces [remove | X | keep]``      Set space handling preference

    ``-n, --newlines [True | False]``         Include newline characters

    ``-d, --space-detect [True | False]``     Convert decrypted Xs to spaces

    ``-g, --group TEXT``                      Set output letter grouping

    ``-c, --select TEXT``                     Select enigma machine configuration

    ``-k, --remember [True | False]``         Remember machine state after encryption
    =====================================     ========================================


reset <configuration>
~~~~~~~~~~~~~~~~~~~~~

Resets specified configuration to "Default" settings.

Basic Examples
--------------

**Create new configuration:**

.. code-block:: bash

    $ enigma new config1 --model M3 --fast 1,2,3 --middle 5,12,23 --slow 2,17,9 --plugs AB,GD,KL,IU --reflect UKW-B

**Encrypt from standard input:**

.. code-block:: bash

    $ enigma pref --select config1
    $ enigma encrypt "Hello World"

    Encrypting  [####################################]  100%
    CMQYT PZVTS

**Encrypt from file input, keeping spaces:**

.. code-block:: bash

    $ enigma encrypt -f /usr/share/dict/words -o ~/Desktop/demo.txt
    Encrypting  [####################################]  100%
    $ less ~/Desktop/demo.txt

    Y
    B
    PV
    U BW
    LEK KW
    BBD 
    LZSO
    V DPGRT PS
    PWZ SXDJL 
    KFIRL 
    RFMNA FT
    QGN KMNTC O
    BZDJ SQDT
    C VXCAP BTQ
    .
    .
    .
