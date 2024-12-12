# Solidity Detectors POC: Static Analysis Tool

Solidity Detectors POC is an open source tool to assist Solidity developers and auditors in the detection of smart contract vulnerabilities. It modifies the Slither Static Analyzer by adding 3 new detectors and modifying an existing one. 

## Quick Start

### Install Solidity Detectors POC

Solidity Detectors POC is built upon the Slither Static Analyzer. Installing Solidity Detectors POC requires the user to install [Slither](https://github.com/crytic/slither).

> **Note** <br />
> Slither requires Python 3.8+.
> If you're **not** going to use one of the [supported compilation frameworks](https://github.com/crytic/crytic-compile), you need [solc](https://github.com/ethereum/solidity/), the Solidity compiler; we recommend using [solc-select](https://github.com/crytic/solc-select) to conveniently switch between solc versions.

**Use Git to clone the Solidity Detectors POC repository.**

```bash
git clone https://github.com/crytic/slither.git && cd slither
python3 -m pip install .
```

We recommend using a Python virtual environment, as detailed in the [Developer Installation Instructions](https://github.com/trailofbits/slither/wiki/Developer-installation).

### Run Solidity Detectors POC

Once you've cloned the repository and installed the necessary dependencies to run Slither, you can start running the static analyzer on your smart contracts. Solidity Detectors POC is to be run from the root of the cloned repository.

```
python3 -m slither path/to/your/directory/or/file.sol
```
To run files that use dependencies, add the following parameter:
```
python3 -m slither path/to/your/directory/or/file.sol --solc-remaps "@dependencies=path/to/your/dependencies/@dependencies"
```

### Run Slither with our detectors

- Link `slither-testsuite-measurement/our_detectors` to the `slither/detectors` folder.
  In `slither/detectors`:

```bash
ln -s ../../slither-testsuite-measurement/our_detectors our_detectors
```

- Add new detectors in `slither/detectors/all_detector.py` file.

- Run slither:

```bash
python3 -m slither $PATH_TO_PROJECT
```

- With dependencies example:

```bash
python3 -m slither $PATH_TO_PROJECT --solc-remaps "@openzeppelin=node_modules/@openzeppelin @dlsl=node_modules/@dlsl" --exclude-dependencies
```

- To run only one file:

```bash
python3 -m slither $PATH_TO_PROJECT --include-paths $PATH_TO_FILE
```

### Slither testsuite measurement

- Create a new detector in `/our_detectors` folder and import it in `runner.py`
- Add it to `all_detector_classes` dictionary
