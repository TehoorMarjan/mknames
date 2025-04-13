# mknames

`mknames` is a Python tool for generating first names and last names based on French and USA statistics. It uses data from the INSEE database, USA sources, and other datasets to create names with realistic distributions.

## Features

- Generate boy and/or girl names.
- Specify the number of names to generate.
- Allow or disallow duplicate names.
- Use a custom seed for reproducibility.
- Specify the country for name generation (France or USA).
- Clear the cache if needed.

## Installation

To install `mknames`, ensure you have Python 3.12 or higher, and run:

```bash
pip install mknames
```

## Usage

`mknames` is a command-line tool. Below are some examples of how to use it:

### Basic Usage

Generate 10 boy names and 10 girl names from France:

```bash
mknames -b 10 -g 10 -c fra
```

Generate 5 boy names and 5 girl names from the USA:

```bash
mknames -b 5 -g 5 -c usa
```

### Options

- `-b, --boys <int>`: Number of boy names to generate. `[x>=0]`
- `-g, --girls <int>`: Number of girl names to generate. `[x>=0]`
- `-c, --country [fra|usa]`: Country code. `[default: fra]`
- `-d, --firstname-duplicates`: Allow duplicates on first names.
- `-D, --lastname-duplicates`: Allow duplicates on last names.
- `-s, --seed <int>`: Use a custom seed for reproducibility.
- `-N, --no-cache`: Clear cache.

**Note:** The `-c` flag is now used for specifying the country. Use `-N` to clear the cache. Backward compatibility is not maintained.

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
