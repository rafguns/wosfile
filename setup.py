# coding: utf-8
from setuptools import setup

long_description = open('README.md').read()

setup(
    name='wosfile',
    version='0.4.2',
    url='http://github.com/rafguns/wosfile',
    license='New BSD License',
    author='Raf Guns',
    tests_require=['nose'],
    author_email='raf.guns@uantwerpen.be',
    description='Handle Thomson Reuters Web of Science™ export files',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['wosfile'],
    platforms='any',
    classifiers=[
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development',
        'Topic :: Scientific/Engineering',
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Operating System :: OS Independent',
    ]
)
