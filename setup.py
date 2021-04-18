from setuptools import setup

APP = ['shell_assistant.py']
DATA_FILES = ['shell_assistant_logo.icns', 'config.json']
OPTIONS = {'argv_emulation': False,
           'iconfile': 'shell_assistant_logo.icns',
           'packages': ['pynput']
           }

setup(
    app=APP,
    name='Shell Assistant',
    version='1.3',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    license='Open source',
    author='Nour SIDAOUI',
    author_email='nour@sidaoui.fr',
    setup_requires=['py2app'],
    install_requires=['pynput']
)
