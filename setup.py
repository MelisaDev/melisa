import re

from setuptools import setup


def long_description():
    with open("README.md") as fp:
        return fp.read()


def parse_requirements_file(path):
    with open(path, encoding='utf-8') as file:
        return file.read().splitlines()


with open('melisa/__init__.py', encoding='utf-8') as file:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', file.read(), re.MULTILINE).group(1)


packages = [
    'melisa',
    'melisa.listeners',
    'melisa.models',
    'melisa.models.app',
    'melisa.models.guild',
    'melisa.models.message',
    'melisa.models.user',
    'melisa.utils',
    'melisa.core'
]

setup(
    name='melisa',
    author='MelisaDev',
    url='https://github.com/MelisaDev/melisa',
    version=version,
    packages=packages,
    license='MIT',
    description='Cache-optimized Discord microframework for Python 3',
    long_description=long_description(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    python_requires='>=3.8,<3.11',
    install_requires=parse_requirements_file("requirements.txt"),
    extras_require={
        "speedup": parse_requirements_file("packages/speed.txt")
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Communications :: Chat",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Typing :: Typed",
    ]
)
