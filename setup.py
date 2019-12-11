
from setuptools import (
    setup,
    find_packages,
)


with open('requirements/main.txt') as file:
    requirements = file.read().splitlines()


setup(
    name='pullenti_client',
    version='0.4.0',
    description='Client for PullentiServer',
    url='https://github.com/pullenti/pullenti-client',
    author='Alexander Kukushkin',
    author_email='alex@alexkuk.ru',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing :: Linguistic',
    ],
    keywords='natural language processing, named entity recognition',
    packages=find_packages(),
    install_requires=requirements
)
