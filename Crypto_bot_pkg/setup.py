from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()


# AlexisDaniels:
setup(name = "crypto-Alexis",
    version = 0.0.1
    author = Alexis,
    author_email = alexis_daniels@hotmail.com,
    description = "A package where you can keep track of your favorite cryptocurrencies and obtain buy/sell suggestion based on sentiment analysis of influencers",
    long_description = file: README.md,
    long_description_content_type = text/markdown,
    keywords = 'crypto', 'algotrade',
    license = 'MIT',
    url = https://github.com/Programming-The-Next-Step-2021/Weather-app,
    classifiers = [
        Programming Language :: Python :: 3,
        License :: OSI Approved :: MIT License,
        Operating System :: OS Independent,
    ]
    package_dir =
        = src
    packages = [packages],
    python_requires = >=3.6