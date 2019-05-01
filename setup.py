#!/usr/bin/python3

from sys import version_info
from setuptools import setup

if version_info < (3, 5, 3):
    raise RuntimeError("pulsar2 requires Python 3.5.3+")

setup(
    name='pulsar2',
    version='1.0',
    description='Pulsar2 is actor framework',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Development Status :: 4 - Beta',
#        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
    ],
    author='Vitold Sedyshev',
    author_email='vit1251@gmail.com',
    maintainer=', '.join([
        'Vitold Sedyshev <vit1251@gmail.com>',
    ]),
    maintainer_email='pulsar2@googlegroups.com',
    url='https://github.com/vit1251/pulsar2',
    project_urls={
#        'CI: Travis': '...',
#        'Coverage: codecov': '...',
#        'GitHub: issues': '',
#        'GitHub: repo': '',
    },
    license='MIT',
    packages=['pulsar2'],
    python_requires='>=3.5.3',
    install_requires=['aiohttp'],
)
