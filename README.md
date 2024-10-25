# PyL2BV-CLI

PyL2BV-CLI is a command-line interface for running models using the PyL2BV library.

## Installation

You can install the package directly from GitHub using pip:

```sh
pip install git+https://github.com/LFT-W47/PyL2BV.git
```

## Usage

### Using the Python API

To run a model using the Python API, you can use the `run_pyl2bv.py` script. Below is an example of how to use it:

```python
from PyL2BVcli.model_runner import run_model

# Define the input folder path
input_folder_path = "/path/to/your/input_folder"

# Define the input type (assuming it's a required argument)
input_type = "CHIME netCDF"

# Define the model folder path
model_name = "/path/to/your/model_folder"

# Define the conversion factor (example value, replace with actual if needed)
conversion_factor = 0.0001

# Run the model
run_model(
    input_folder_path=input_folder_path,
    input_type=input_type,
    model_folder_path=model_name,
    conversion_factor=conversion_factor,
    plot=False,
)
```

### Using the Command-Line Interface (CLI)

You can also run the model using the command-line interface. Below is an example of how to use it:

```sh
python -m PyL2BVcli.cli /path/to/your/input/folder "CHIME netCDF" /path/to/your/model/folder 0.0001 --plot
```

The CLI accepts the following arguments:

- `input_folder_path`: Path to the input folder
- `input_type`: Type of input file
- `model_folder_path`: Path to the model folder
- `conversion_factor`: Image conversion factor
- `--plot`: Optional flag to enable plotting

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
