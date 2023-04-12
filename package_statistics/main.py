import gzip
from argparse import ArgumentParser
from io import BytesIO
from typing import Dict
from urllib.error import URLError
from urllib.request import urlopen

DEFAULT_MIRROR = "http://ftp.uk.debian.org/debian/dists/stable/main"
N_PACKAGES = 10


def download_file(url: str) -> bytes:
    """
    Downloads a file from a URL and returns the contents as bytes.

    Attributes
    ----------
    url : str
        The URL to download the file from.

    Returns
    -------
    bytes
        The contents of the file as bytes.

    Raises
    ------
    URLError
        If the url is invalid.
    """
    print(f"Downloading {url}")

    with urlopen(url) as response:
        return response.read()


def parse_debian_contents_file(content_file: str) -> Dict[str, int]:
    """
    Parses a Debian Contents file and returns a dictionary of package names and their number of files.

    Attributes
    ----------
    content_file : str
        The contents of a Debian Contents file.

    Returns
    -------
    Dict[str, int]
        A dictionary of package names and their number of files.
    """
    package_stats = {}

    # Split the whole text in lines
    for line in content_file.splitlines():
        # Split each line into space separated parts.
        parts = line.split()

        # Avoid packages that don't follow the pattern of two columns.
        # The first column is the file path, the second is the list of package names separated by comma
        if len(parts) == 2:
            # Find all packages separated by comma
            for package_name in parts[1].split(","):
                # Add one to the file counter
                package_stats[package_name] = package_stats.get(package_name, 0) + 1

    return package_stats


def summarize_package_statistics(statistics: Dict[str, int], top_n: int = 10) -> None:
    """
    Prints the top 10 packages with the most files.

    Attributes
    ----------
    statistics : Dict[str, int]
        A dictionary of package names and their number of files.
    top_n : int
        The number of packages to display.

    Raises
    ------
    ValueError
        If the top number of packages to display is less than or equal to 0.
    """
    if top_n <= 0:
        raise ValueError("The number of packages to display cannot be less than or equal to 0.")

    # Sort packages by the number of files associated with
    sorted_packages = sorted(statistics.items(), key=lambda x: x[1], reverse=True)

    # Find the total number of packages
    total_packages = len(sorted_packages)

    # If the top_n value provided is bigger than the number of packages, make top_n print all packages
    if top_n >= total_packages:
        top_n = total_packages
        print(f"Displaying all {total_packages} packages.")

    # Find the size of the biggest package name to print
    biggest_package_name = max([len(item[0]) for item in sorted_packages[:top_n]])

    # Calculates the size of spaces to give
    spaces = biggest_package_name + 10

    # Prints top_n packages with a left-justified wide field with size of the spaces variable
    print(f"{'package name':<{spaces}}number of files")
    for package_name, file_count in sorted_packages[:top_n]:
        print(f"{package_name:<{spaces}}{file_count}")


def decompress_gz_file(compressed_content: bytes) -> str:
    """
    Decompress a GZ file and returns the contents as a string.

    Parameters
    ----------
    compressed_content : bytes
        The compressed content of a GZ file.

    Returns
    -------
    str
        The uncompressed content of the GZ file.

    Raises
    ------
    BadGzipFile
        If the content bytes aren't compressed with Gz.
    """
    with gzip.open(BytesIO(compressed_content), "rb") as file:
        return file.read().decode("utf-8")


def main():
    # Parse CLI args
    parser = ArgumentParser(
        description="""
            Display package names with the number of files associated with them 
            for a given Debian mirror and architecture.
        """
    )
    parser.add_argument(
        "arch",
        type=str,
        help="The binary architecture or the pseudo-architecture of the Debian system (e.g. amd64, arm64, mips).",
    )
    parser.add_argument(
        "-u",
        "--udeb",
        action="store_true",
        help="To search for udeb instead of normal Contents file.",
    )
    parser.add_argument(
        "-m",
        "--mirror",
        type=str,
        help=f"The mirror to search for the Contents file. Default is {DEFAULT_MIRROR}.",
        default=DEFAULT_MIRROR,
    )
    parser.add_argument(
        "-n",
        "--number-of-packages",
        type=int,
        help=f"The number of packages to display. Default is {N_PACKAGES}.",
        default=N_PACKAGES,
    )

    args = parser.parse_args()

    # Contents URL
    sarch = f"udeb-{args.arch}" if args.udeb else args.arch
    debian_mirror_url = f"{args.mirror}/Contents-{sarch}.gz"

    try:
        # Download and extract the Contents file
        content_file_as_gz = download_file(debian_mirror_url)
        content_file = decompress_gz_file(content_file_as_gz)

        # Calculate the number of files associated with each package and print the biggest ones
        package_stats = parse_debian_contents_file(content_file)
        summarize_package_statistics(package_stats, args.number_of_packages)
    except URLError as e:
        print(f"Error downloading {debian_mirror_url}: {e}")
    except Exception as e:
        print(f"Error processing file: {e}")


if __name__ == "__main__":
    main()
