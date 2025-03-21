from setuptools import find_packages, setup

setup(
    name="enchante",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "typer",
        "rich",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "enchante=enchante.cli:app",
        ],
    },
    description="Enchante - A modular penetration testing framework",
    author="Clery Arque-Ferradou",
    author_email="clery.arqueferradou@gmail.com",
    url="https://github.com/cleeryy/enchante",
    python_requires=">=3.6",
)
