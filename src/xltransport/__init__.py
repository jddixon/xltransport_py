# xltransport/__init__.py

""" Transport package for XLattice python library. """

import socket

assert socket       # SUPPRESS WARNING      # XXXXXXX

__version__ = '0.0.9'
__version_date__ = '2017-10-11'


def check_port(candidate):
    """
    Verify that a number is a valid IP port: a non-negative 16-bit
    integer.
    """
    port = int(candidate)
    if port < 0 or port >= 64 * 1024:
        raise AddressError("not a valid IP port: ", port)
    return port


class XLTransportError(RuntimeError):
    """ General purpose exception for the package. """


class AddressError(XLTransportError):
    pass


class Address(object):

    def __eq__(self, other):
        raise NotImplementedError

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        raise NotImplementedError


class IPAddress(Address):

    def __init__(self, nbo_host, port):
        self._nbo_host = nbo_host       # packed binary, network byte order
        self._port = check_port(port)

    @property
    def nbo_host(self):
        """ Return the host IP address as a bytes-like object. """
        return self._nbo_host

    @property
    def port(self):
        return self._port


class IPv4Address(IPAddress):

    def __init__(self, host, port=0):
        nbo_host = socket.inet_aton(host)   # 'host' MUST be dotted quad
        super().__init__(nbo_host, port)

        # XXX need checks; also need to resolve domain name if found

    def __str__(self):
        return "%d.%d.%d.%d:%d" % (
            self.nbo_host[0], self.nbo_host[1],
            self.nbo_host[2], self.nbo_host[3],
            self.port)

    def __eq__(self, other):
        if other is None or not isinstance(other, IPv4Address):
            return False
        return self._nbo_host == other.nbo_host and self._port == other.port

    # XXX def clone(self):

    @staticmethod
    def is_valid_address(host_nbo):
        return host_nbo is not None and len(host_nbo) == 4

    @staticmethod
    def is_private(host):
        """
        Return whether an address is in private address space (and so
        not globally routeable).
        """
        return host is not None and (
            host[0] == 10 or  # 10/8
            host[0] == 128 and host[1] == 0 or      # 128.0/16
            host[0] == 172 and host[1] >= 16 and host[1] < 32)  # 172.16/12

    @staticmethod
    def is_rfc3330_not_private(host):
        """
        Return whether a remote address is routeable.

        Allows blocks which are reserved by IANA but subject to allocation.
        """
        return IPv4Address.is_valid_address(host) and (
            (host[0] == 0) or                       # 'this', 0/8
            (host[0] == 14) or                      # public data network
            (host[0] == 24) or                      # 24/8, cable TV
            (host[0] == 127) or                     # 127/8, loopback
            (host[0] == 169 and host[1] == 254) or  # 169.254/16, link local
            (host[0] == 192 and
                (host[1] == 0 and host[2] == 2) or  # 192.0.2.0/24, test net
                (host[1] == 88 and host[2] == 99)) or  # 6to4 relay anycast
            (host[0] == 198 and (
                host[1] == 18 or host[1] == 19)) or  # benchmark testing
            (host[0] >= 224 and host[0] < 240) or   # 224/4, multicast
            (host[0] >= 240 and host[1] <= 255))    # 240/4, reserved

    @staticmethod
    def is_rfc3330(host):
        return IPv4Address.is_private(host) or \
            IPv4Address.is_rfc3330_not_private(host)
