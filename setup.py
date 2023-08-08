import pathlib
import re
import setuptools

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text(encoding="utf8")

with open(HERE / "melisa/__init__.py") as file:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', file.read(), re.MULTILINE
    ).group(1)

setuptools.setup(
    name="melisa",
    author="MelisaDev",
    url="https://github.com/MelisaDev/melisa",
    version=version,
    packages=setuptools.find_packages(),
    license="MIT",
    description="Cache-optimized Discord microframework for Python 3",
    long_description=README,
    long_description_content_type="text/markdown",
    include_package_data=True,
    python_requires=">=3.8,<3.11",
    zip_safe=False,
    install_requires=["aiohttp", "typing_extensions"],
    extras_require={"speedup": ["orjson==3.9.4"]},
    test_suite="tests",
    project_urls={
        "Documentation": "https://docs.melisapy.site/",
        "Source (GitHub)": "https://github.com/MelisaDev/melisa",
        "Discord": "https://discord.gg/QX4EG8f7aD",
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
    ],
)
