from setuptools import setup



setup(
    name='EnigmaMachine',
    author='cjengdahl',
    author_email='cjengdahl@gmail.com',
    version='0.1',
    py_modules=['enigma', 'enigma_machine', 'rotor', 'reflect', 'plugboard', 'enigma_exceptions', 'configsparser'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        enigma=enigma:cli
    '''
)