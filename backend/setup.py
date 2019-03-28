from distutils.core import setup

setup(
    name='WhatBot Backend',
    version='0.0.1',
    description='WhatBot backend modules',
    packages=['conf',
              'data_extractor',
              'database',
              'query_module',
              'response_module',
              'utility_module']
)
