#!/usr/bin/env python3

import monk
from distutils.core import setup


setup(name='monk',
      version=monk.__version__,
      description='Monk detective',
      package_data={'': ['*.cfg']},
      packages=['monk', 'handlers', 'extractors', ])
