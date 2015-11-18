# coding: utf-8
from setuptools import setup

long_description = open('README.md').read()

setup(
    name='wos',
    version='0.2',
    url='http://github.com/rafguns/wos/',
    license='New BSD License',
    author='Raf Guns',
    tests_require=['nose'],
    install_requires=['unicodecsv==0.13'],
    author_email='raf.guns@uantwerpen.be',
    description='Handle Thomson Reuters Web of Science™ export files',
    long_description=long_description,
    packages=['wos'],
    platforms='any',
    classifiers=[
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development',
        'Topic :: Scientific/Engineering',
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Operating System :: OS Independent',
    ]
)
