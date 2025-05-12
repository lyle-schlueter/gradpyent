# Gradpyent, a Python Gradient Generator

Gradpyent is a Python package for generating color gradients based on list-like inputs and start/end color values. The generated gradients are ideal for data visualization, user interfaces, or anywhere you want to convert a list of values into a color gradient.

This package allows you to specify colors in a variety of formats including RGB, HTML, and KML, giving you the flexibility to match your specific needs. 

The gradient generation algorithm automatically scales input values outside the range of 0-1, ensuring the generated gradient remains consistent and visually pleasing.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [License](#license)
- [Code Quality](#code-quality)
- [Tests](#tests)

## Installation

You can install Gradpyent directly from PyPI:

```bash
pip install gradpyent
```

## Usage

Basic usage:

```python
from gradpyent.gradient import Gradient

# Define the start and end colors as RGB, HTML, or KML
start_color = 'RGB(255,0,0)'  # Red in RGB
end_color = '#0000ff'  # Blue in HTML

# Instantiate the gradient generator, opacity is optional (only used for KML)
gg = Gradient(gradient_start=start_color, gradient_end=end_color, opacity=1.0)

# Define the input list
input_list = [0, 0.5, 1]

# Generate the gradient
gradient = gg.get_gradient_series(series=input_list, fmt='html')

print(gradient)
```

## Examples

Here are some more examples demonstrating how to use different color formats and list inputs:

- RGB colors:

```python
start_color = 'rgb(255,0,0)'  # Red
end_color = 'rgb(0,0,255)'  # Blue
input_list = [0, 0.5, 1]
```

- HTML colors:

```python
start_color = '#ff0000'  # Red
end_color = '#0000ff'  # Blue
input_list = [0, 0.5, 1]
```

- KML colors:

```python
start_color = 'ff0000ff'  # Red
end_color = 'ffff0000'  # Blue
input_list = [0, 0.5, 1]
```

- Scaling input values:

```python
start_color = 'rgb(255,0,0)'  # Red
end_color = '#0000ff'  # Blue
input_list = [-5, 0, 5, 10]  # Values outside 0-1 range
```

- Jupyter notebook samples:
  - See the `notebooks` directory for more examples

## License
This project is licensed under the terms of the MIT license. See the [LICENSE.md](LICENSE.md) file for details.

## Code Quality
> ruff format src/ tests/
>
> ruff check src/ [--fix]
>

## Tests
> pytest --cov


## Docs
sphinx-apidoc -o docs/ src/gradpyent


### Enjoy the colorful world!