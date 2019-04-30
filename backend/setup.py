from distutils.core import setup

setup(
    name='WhatBot Backend',
    version='0.0.2',
    description='WhatBot backend modules',
    packages=['conf',
              'data_extractor',
              'database',
              'query_module',
              'search_module',
              'utility_module',
              'management_module',
              'tests']
)
