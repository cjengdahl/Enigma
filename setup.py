from setuptools import setup


setup(

    # Application name
    name='enigma-cli',

    # Version Number
    version="0.1.4",

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

    license="MIT",
    
    classifiers=[
    'Development Status :: 5 - Production/Stable',

    # Indicate who your project is intended for
    'Intended Audience :: Other Audience',

    # Pick your license as you wish (should match "license" above)
    'License :: OSI Approved :: MIT License',

    # Not compatible with Python2
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    ],

    description="German Cipher Machine Command-Line Tool",

    long_description=open("README.rst").read(),

    # Dependent packages
    install_requires=[
        'Click',
    ],
    
    # Required config files
    # data_files=[('', ['engima/model.ini'])],
    
    package_data={'enigma': ['*.ini']},

    # Executable information
    entry_points='''
        [console_scripts]
        enigma=enigma_driver:cli
    '''


)
