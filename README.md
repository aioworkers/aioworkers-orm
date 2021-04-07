# aioworkers-orm

[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/aioworkers/aioworkers-orm/CI)](https://github.com/aioworkers/aioworkers-orm/actions?query=workflow%3ACI)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aioworkers-orm)](https://pypi.org/project/aioworkers-orm)
[![PyPI](https://img.shields.io/pypi/v/aioworkers-orm)](https://pypi.org/project/aioworkers-orm)

An aioworkers plugin for [orm](https://github.com/encode/orm)
to add `orm.Model` available via `aioworkers.core.context.Context`.

Features:
- Attach model by class reference.
- Create model by specification.

## Development

Install dev requirements:

```shell
poetry install
```

Run tests:

```shell
pytest
```
