import setuptools 

# AlexisDaniels:
setuptools.setup(
    name = "crypto bot",
    version = 0.1, 
    author = "Alexis",
    author_email = "alexis_daniels@hotmail.com",
    description = "A package where you can keep track of your favorite cryptocurrencies and obtain buy/sell suggestion based on the RSI",
    license = 'MIT',
    packages = setuptools.find_packages(),
    install_requires = [
        'numpy',
        'pandas',
        'matplotlib',
        'asyncio',
        'websocket',
        'websockets',
        'asyncio',
        'TA-Lib',
        'tkinter'
    ]
    )
