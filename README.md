## How to install Slither

> **Note** <br />
> Slither requires Python 3.8+.
> If you're **not** going to use one of the [supported compilation frameworks](https://github.com/crytic/crytic-compile), you need [solc](https://github.com/ethereum/solidity/), the Solidity compiler; we recommend using [solc-select](https://github.com/crytic/solc-select) to conveniently switch between solc versions.

### Using Pip

```console
python3 -m pip install slither-analyzer
```

### Using Git

```bash
git clone https://github.com/crytic/slither.git && cd slither
python3 -m pip install .
```

We recommend using a Python virtual environment, as detailed in the [Developer Installation Instructions](https://github.com/trailofbits/slither/wiki/Developer-installation), if you prefer to install Slither via git.

### Using Docker

Use the [`eth-security-toolbox`](https://github.com/trailofbits/eth-security-toolbox/) docker image. It includes all of our security tools and every major version of Solidity in a single image. `/home/share` will be mounted to `/share` in the container.

```bash
docker pull trailofbits/eth-security-toolbox
```

To share a directory in the container:

```bash
docker run -it -v /home/share:/share trailofbits/eth-security-toolbox
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
