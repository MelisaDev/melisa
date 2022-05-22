import re

from setuptools import setup

extras_require = {
    'speed': [
        'orjson>=3.5.4'
    ]
}

requirements = []

with open('requirements.txt', encoding='utf-8') as file:
    requirements = file.read().splitlines()

with open('melisa/__init__.py', encoding='utf-8') as file:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', file.read(), re.MULTILINE).group(1)

if version is None:
    raise RuntimeError('Version is not set!')

readme = ''

with open('README.md', encoding='utf-8') as file:
    readme = file.read()


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
    author='gray-cat, TheMisterSenpai',
    url='https://github.com/MelisaDev/melisa',
    version=version,
    packages=packages,
    license='MIT',
    description='Cache-optimized Discord microframework for Python 3',
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=requirements,
    extras_require=extras_require,
    classifiers=[
        "Development Status :: 1 - Development",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Typing :: Typed",
    ]
)
