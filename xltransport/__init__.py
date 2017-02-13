# xltransport/__init__.py

""" Transport package for XLattice python library. """

__version__ = '0.0.4'
__version_date__ = '2017-02-13'

__all__ = ['__version__', '__version_date__', 'XLTransportError', ]


class XLTransportError(RuntimeError):
    """ General purpose exception for the package. """
