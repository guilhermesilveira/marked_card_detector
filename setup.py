#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = ["opencv-python>=4.5.5.64"]

test_requirements = ['pytest>=3', ]

setup(
    author="Guilherme de Azevedo Silveira",
    author_email='guilherme.silveira@alura.com.br',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A card detector system that uses computer vision implemented using opencv.",
    entry_points={
        'console_scripts': [
            'marked_card_detector=marked_card_detector.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords='marked_card_detector',
    name='marked_card_detector',
    packages=find_packages(include=['marked_card_detector', 'marked_card_detector.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/guilhermesilveira/marked_card_detector',
    version='0.1.0',
    zip_safe=False,
)
