**Since Moibit API services have been discontinued and are no longer available, this new version supports the exact same features but on Pinata ( Decentralised IPFS based storage ) - Same functions as the older matic implementation are supported.**

# Interface Blockchain Network ( IBN )
This project was originally made as a part of the SHAGUN project which we were working on so as to facilitate proper encoding and security of transactions and also maintaining a permanant record of the posts and transactions on the Matic BlockChain Network using the [Moibit API](https://www.moibit.io/) . This repository has now been made public and anyone is free to use the Interface and get easy access to reading and writing securely to and from the Blockchain ( in case you are making your own transaction system ) .

# Main Files
1. **matic_blockchain_interface.py** - Contains the various functions used by the IBN to interact and fetch data from the Moibit API

2. **vendor.py** - Contains the various vendor / helper functions which are required by the IBN

3. **server.py** - This is the main flask file on which our API runs . It contains the various endpoints which the user can query and receive the required data. 

# Requirements
The given code has been written on VSCode , Windows 64-bit , Intel i7 10th gen processor and Python version : 3.9.0 . It should be compatible and must be able to run on any Python 3.x version as well , but for stability concerns it is recommended to use Python 3.5.0 and above .

## Modules :

- [x] `appdirs==1.4.4`
- [x] `base58==2.1.0`
- [x] `black==20.8b1`
- [x] `certifi==2020.12.5`
- [x] `cffi==1.14.5`
- [x] `chardet==4.0.0`
- [x] `click==7.1.2`
- [x] `cryptography==3.4.6`
- [x] `Flask==1.1.2`
- [x] `idna==2.10`
- [x] `itsdangerous==1.1.0`
- [x] `Jinja2==2.11.3`
- [x] `MarkupSafe==1.1.1`
- [x] `mnemonic==0.19`
- [x] `mypy-extensions==0.4.3`
- [x] `pathspec==0.8.1`
- [x] `pycparser==2.20`
- [x] `pycryptodome==3.10.1`
- [x] `pysodium==0.7.7`
- [x] `regex==2021.3.17`
- [x] `requests==2.25.1`
- [x] `toml==0.10.2`
- [x] `tqdm==4.59.0`
- [x] `typed-ast==1.4.2`
- [x] `typing-extensions==3.7.4.3`
- [x] `urllib3==1.26.4`
- [x] `Werkzeug==1.0.1`


The same have also been frozen to a requirements.txt file and can be easily installed from there . Also it is recommended to use a virtual environment to avoid conflicts. This project was developed in a `venv` generated virtual environment .

#

Made By [Ansh Sarkar](https://www.linkedin.com/in/ansh-sarkar/) a.k.a SeraphimCoder
