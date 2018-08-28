import os
import re

from setuptools import setup

# Get version this way, so that we don't load any modules.
with open('./userdefinedfields/__init__.py') as f:
    exec(re.search(r'VERSION = .*', f.read(), re.DOTALL).group())

try:
    setup(
        name='django-user-defined-fields',
        packages=['userdefinedfields'],
        version=__version__,
        description="Simple user defined fields with JSON Field.",
        long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
        license='BSD',
        author='Uptick',
        author_email='dev@uptickhq.com',
        url='https://github.com/uptick/django-user-defined-fields',
        keywords=['jsonfield', ],
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Web Environment',
            'Intended Audience :: Developers',
            'Natural Language :: English',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.6',
        ],
        install_requires=[
            'django',
        ],
        tests_require=[
        ],
    )
except NameError:
    raise RuntimeError("Unable to determine version.")
