# philiprehberger-progress-map

[![Tests](https://github.com/philiprehberger/py-progress-map/actions/workflows/publish.yml/badge.svg)](https://github.com/philiprehberger/py-progress-map/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/philiprehberger-progress-map.svg)](https://pypi.org/project/philiprehberger-progress-map/)
[![License](https://img.shields.io/github/license/philiprehberger/py-progress-map)](LICENSE)
[![Sponsor](https://img.shields.io/badge/sponsor-GitHub%20Sponsors-ec6cb9)](https://github.com/sponsors/philiprehberger)

Parallel map with a built-in terminal progress bar.

## Installation

```bash
pip install philiprehberger-progress-map
```

## Usage

```python
from philiprehberger_progress_map import pmap

def process(x):
    return x * 2

results = pmap(process, range(100))
```

Use multiprocessing instead of threading:

```python
results = pmap(process, range(100), mp=True, workers=8)
```

Customize the progress display:

```python
results = pmap(process, items, label="Processing", show_progress=True)
```

## API

### `pmap(func, items, *, workers=4, mp=False, label="", show_progress=True)`

| Parameter       | Type               | Default | Description                                  |
| --------------- | ------------------ | ------- | -------------------------------------------- |
| `func`          | `Callable[[T], R]` | —       | Function to apply to each item               |
| `items`         | `Iterable[T]`      | —       | Iterable of items to process                 |
| `workers`       | `int`              | `4`     | Number of worker threads or processes        |
| `mp`            | `bool`             | `False` | Use multiprocessing instead of threading     |
| `label`         | `str`              | `""`    | Optional label prefix for the progress bar   |
| `show_progress` | `bool`             | `True`  | Whether to display the progress bar          |

**Returns:** `list[R]` — Results in the same order as the input items.


## Development

```bash
pip install -e .
python -m pytest tests/ -v
```

## License

MIT
