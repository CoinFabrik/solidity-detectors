# Solidity Detectors: Static Analysis Tool

Solidity Detectors is an open source tool to assist Solidity developers and auditors in the detection of smart contract vulnerabilities. It modifies the Slither Static Analyzer by adding 3 new detectors and modifying an existing one. 

## Quick Start

### Install Solidity Detectors

Solidity Detectors is built upon the Slither Static Analyzer. Installing Solidity Detectors requires the user to install [Slither](https://github.com/crytic/slither).

> **Note** <br />
> Slither requires Python 3.8+.
> If you're **not** going to use one of the [supported compilation frameworks](https://github.com/crytic/crytic-compile), you need [solc](https://github.com/ethereum/solidity/), the Solidity compiler; we recommend using [solc-select](https://github.com/crytic/solc-select) to conveniently switch between solc versions.

#### Use a Python Virtual Environment

It is recommended to use a Python virtual environment to prevent version conflicts. For more information on Python environments for Slither, you can consult the [Developer Installation Instructions](https://github.com/trailofbits/slither/wiki/Developer-installation). 

You will need to install virtualenv to create and manage your Python virtual environments.

```bash
pip install virtualenv
```

You should set up the virtual environment in the parent directory of Solidity Detectors or in any higher-level directory within the directory tree. 

Navigate to the folder where you wish to create your virtual environment. It is advisable to create a **project directory** where you will create your virtual environment and clone **Solidity Detectors**. Then, create your environment with the following command:

```bash
python -m venv virtual-environment-name
```

Every time you wish to activate the virtual environment, you can run this command:

```bash
source virtual-environment-name/bin/activate
```

To deactivate the virtual environment, simply run

```bash
deactivate
```

All the necessary installations to run Slither and Solidity Detectors will be managed from the virtual environment.

#### Use Git to clone the Solidity Detectors POC repository

Navigate to the project directory. Then, clone **Solidity Detectors**.

```bash
git clone https://github.com/crytic/slither.git && cd slither
python3 -m pip install .
```
#### Install and Use a solc Version

To analyze your smart contracts, you will need to install and use the necessary solc version. First, make sure that solc is installed.

```bash
npm install solc
```

Then, identify the solc version used by your contract and install it using the following commands.

```bash
solc-select install your-version
solc-select use your-version
```
### Run Solidity Detectors POC

Once you've cloned the repository and installed the necessary dependencies to run Slither, you can start running the static analyzer on your smart contracts. 

> ⚠️ **Important**  <br />
>**Solidity Detectors** is to be run from the root of the cloned solidity_detectors repository. Running the tool from another directory will result in errors or will use Slither without our Solidity Detectors if a global version of Slither is installed.

You can run the tool on repositories and .sol files alike. Consider the following example for running the tool on a file by using the `slither` command:

``
python3 -m slither path/to/your/directory/or/file.sol
``
To run files that use dependencies, add the `--solc-remaps` parameter:
```
python3 -m slither path/to/your/directory/or/file.sol --solc-remaps "@dependencies=path/to/your/dependencies/@dependencies"
```
