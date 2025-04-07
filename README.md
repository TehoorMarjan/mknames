# mknames

`mknames` is a Python tool for generating first names and last names based on French statistics. It uses data from the INSEE database and other sources to create names with realistic distributions.

## Features

- Generate boy and/or girl names.
- Specify the number of names to generate.
- Allow or disallow duplicate names.
- Use a custom seed for reproducibility.
- Clear cache for fresh data.

## Installation

To install `mknames`, ensure you have Python 3.12 or higher, and run:

```bash
pip install mknames
```

## Usage

`mknames` is a command-line tool. Below are some examples of how to use it:

### Basic Usage

Generate 10 boy names and 10 girl names:

```bash
mknames -b 10 -g 10
```

### Options

- `-b, --boys <int>`: Number of boy names to generate.
- `-g, --girls <int>`: Number of girl names to generate.
- `-d, --firstname-duplicates`: Allow duplicate first names.
- `-D, --lastname-duplicates`: Allow duplicate last names.
- `-s, --seed <int>`: Use a custom seed for reproducibility.
- `-c, --no-cache`: Clear cache before generating names.

### Interactive Mode

If no options are provided, `mknames` will prompt you interactively:

```bash
mknames
```

## Development

To contribute to `mknames`, clone the repository and install the development dependencies:

```bash
git clone <repository-url>
cd mknames
pdm install --dev
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Author

Tehoor Marjan (<tehoor.marjan@gmail.com>)
