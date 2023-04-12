# Debian Package Statistics

Display package names with the number of files associated with them for a given Debian mirror and architecture.

This command line tool downloads and parses the Debian Contents file to calculate the package statistics.

## Requirements

- Python 3.x

## Installation

Before installing the CLI, you will need [poetry](https://python-poetry.org/docs/#installation) or you can call the `package_statistics/main.py` file directly.

To install it, enter the repository and run `poetry install`.

After that, you can call the CLI with `poetry run package_statistics` or run `poetry shell` and then `package statistics`.

## Usage

```bash
usage: package_statistics [-h] [-u] [-m MIRROR] [-n NUMBER_OF_PACKAGES] arch

positional arguments:
  arch                  The binary architecture or the pseudo-architecture of the Debian system (e.g. amd64, arm64, mips).

optional arguments:
  -h, --help            show this help message and exit
  -u, --udeb            To search for udeb instead of normal Contents file.
  -m MIRROR, --mirror MIRROR
                        The mirror to search for the Contents file. Default is http://ftp.uk.debian.org/debian/dists/stable/main.
  -n NUMBER_OF_PACKAGES, --number-of-packages NUMBER_OF_PACKAGES
                        The number of packages to display. Default is 10.
```

### Example

```bash
package_statistics amd64
```
or

```bash
python package_statistics/main.py amd64
```
Results:

```bash
package name                                                    number of files
devel/piglit                                                    51784
science/esys-particle                                           18015
libdevel/libboost1.74-dev                                       14332
math/acl2-books                                                 12668
golang/golang-1.15-src                                          9015
libdevel/liboce-modeling-dev                                    7457
net/zoneminder                                                  7002
libdevel/paraview-dev                                           6178
kernel/linux-headers-5.10.0-20-amd64                            6162
kernel/linux-headers-5.10.0-18-amd64                            6156
```

## Development

> It took me approximetly 5 hours to deliver this project.

My approach to the problem was:
1. Read about the format of a Contents file.
2. Created a base project with poetry and static code linter.
3. Created the base structure of a command-line program that was able to receive arguments, download a file, extract that file, and print the result.
4. Implemented the download file method and the Gz extract file methods.
5. Implemented the Contents file parser method and the function to sort and print the packages with most files associated with.
6. Added the command-line arguments and construct the URL of the Contents file based on the architecture and the Debian mirror.
7. Added new arguments to allow the user to specify a different Debian mirror or different number of packages to display.
8. Added unit tests for the core methods.
9. Read about the format of a Contents file again to guarantee that everything is right.
10. Created this README.

### Testing

To run the tests, simply run the command:

```bash
make tests
```

### Static Code Analysis

To run the code linter, simply run the command:

```bash
make code_review
```
