from setuptools import setup

setup(name='server-sleep-coreplugins',
      version='0.1',
      description='These are the base plugins for server-sleep.',
      url='https://github.com/SLCoding/server-sleep-coreplugins',
      author='SourceLan',
      author_email='schuette.marcus@googlemail.com',
      license='MIT',
      packages=['server_sleep_coreplugins.pingcheck',
                'server_sleep_coreplugins.plexcheck',
                'server_sleep_coreplugins.proccheck',
                'server_sleep_coreplugins.pyloadcheck',
                'server_sleep_coreplugins.usercheck'],
      install_requires=[
          'server-sleep',
          'server-sleep-api',
          'configparser'
      ],
      zip_safe=False)
