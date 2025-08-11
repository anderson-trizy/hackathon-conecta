"""
Adapters para diferentes clouds.
"""

from .interfaces import DataSourceInterface, MLInterface, StorageInterface

__all__ = [
    'DataSourceInterface',
    'MLInterface', 
    'StorageInterface'
]
