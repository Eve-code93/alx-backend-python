#!/usr/bin/env python3
"""Utils module containing utility functions."""
from typing import Mapping, Any, Sequence, Union
import requests


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """Access nested map with a sequence of keys."""
    for key in path:
        nested_map = nested_map[key]
    return nested_map
