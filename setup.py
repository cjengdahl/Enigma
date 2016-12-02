from setuptools import setup


setup(

    # Application name
    name='EnigmaMachine',

    # Version Number
    version="0.1.0",

    # Author details
    author='cjengdahl',
    author_email='cjengdahl@gmail.com',

    # Packages
    packages=['enigma'],

    # CLI module
    py_modules=['enigma_driver'],

    # Include additional files with package
    include_package_data=True,

    # Details
    # Put pypi url here

    license="LICENSE.txt",

    description="German Encryption Machine",

    long_description=open("README.txt").read(),

    # Dependent packages
    install_requires=[
        'Click',
    ],
    
    # Required config files
    data_files=[('', ['config/config.ini', 'engima/model.ini'])],

    # Executable information
    entry_points='''
        [console_scripts]
        enigma=enigma_driver:cli
    '''


)
