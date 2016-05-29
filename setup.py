from setuptools import setup

setup(name='remorse',
      version='0.1',
      description='Morse code player',
      url='http://github.com/jhobbs/remorse',
      author='Jason Hobbs',
      author_email='jason.hobbs@gmail.com',
      license='Apache License 2.0',
      packages=['remorse'],
      install_requeres=['audiogen'],
      scripts=['scripts/remorse'])
