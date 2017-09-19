#!/usr/bin/env python3
# xltransport_py/test_basics.py

""" Exercise code handling IPv4 addresses. """

# import hashlib
# import os
import time
import unittest

from rnglib import SimpleRNG
from xltransport import IPv4Address, AddressError


class TestIPv4Address(unittest.TestCase):
    """ Exercise code handling IPv4 addresses. """

    A1234 = '1.2.3.4'
    A1235 = '1.2.3.5'

    def setUp(self):
        self.rng = SimpleRNG(time.time())
        self.v4addr = None
        self.v4addr2 = None

    def tearDown(self):
        pass

    def test_bad_addr(self):
        try:
            IPv4Address("1.2.3.4", -92)
            self.fail("didn't catch out of range port number -92")
        except AddressError:
            # success
            pass
        try:
            IPv4Address("1.2.3.4", 65536)
            self.fail("didn't catch out of range port number 2^16")
        except AddressError:
            # success
            pass
        try:
            IPv4Address("1.2.3.4.5", 5)
            self.fail("didn't catch 1.2.3.4.5")
        # except AddressError:
        except OSError:
            # success
            pass

        # XXX SPECIFICATION ERROR: arg should be bytes-like
#       self.assertFalse(IPv4Address.is_valid_address(None))
#       self.assertFalse(IPv4Address.is_valid_address("0"))
#       self.assertFalse(IPv4Address.is_valid_address("0.0"))
#       self.assertFalse(IPv4Address.is_valid_address("0.0.0"))
#       self.assertTrue(IPv4Address.is_valid_address("0.0.0.0"))
#       self.assertFalse(IPv4Address.is_valid_address("0.0.0.0.0"))

    def testV4AddrWithPort(self):
        v4addr = IPv4Address(self.A1234, 97)
        self.assertIsNotNone(v4addr)
        self.assertEqual(97, v4addr.port)

        # HACKED FROM JAVA, NEEDS CLEANING UP
#       iaddr = v4addr.get_inet_address()   # InetAddress
#       byte_addr = v4addr.get_ip_address()
#       self.assertEqual(4, byte_addr.length)
#       addr_from_ia = iaddr.get_address()
#       self.assertEqual(4, addr_from_ia.length)
#       for ndx in range(4):
#           self.assertEqual(byte_addr[ndx], addr_from_ia[ndx])
#       v4addr2 = IPv4Address(byte_addr, 97)
#       self.assertIsNotNone(v4addr2)
#       self.assertEqual(v4addr, v4addr2)
#       self.assertEqual("1.2.3.4:97", v4addr2.__str__())

    def test_equal(self):
        v4addr = IPv4Address(self.A1234, 52)
        self.assertEqual(v4addr, v4addr)

        v4addr2 = IPv4Address(self.A1235, 52)    # different IP
        self.assertIsNotNone(v4addr)
        self.assertFalse(v4addr == v4addr2)
        v4addr2 = IPv4Address(self.A1234, 53)    # different port
        self.assertFalse(v4addr == v4addr2)
        v4addr2 = IPv4Address(self.A1234, 52)    # same IP and port
        self.assertEqual(v4addr, v4addr2)

    def test_private_ips(self):
        # Web server running in 10/8
        v4addr = IPv4Address("10.0.0.1", 80)
        addr = v4addr.nbo_host
        self.assertEqual(10, addr[0])
        self.assertEqual(0, addr[1])
        self.assertEqual(0, addr[2])
        self.assertEqual(1, addr[3])
        self.assertTrue(IPv4Address.is_private(addr))
        self.assertEqual(80, v4addr.port)

        # Web server running in 128.0/16
        v4addr = IPv4Address("128.0.12.121", 8080)
        addr = v4addr.nbo_host
        self.assertEqual(128, addr[0])
        self.assertEqual(0, addr[1])
        self.assertEqual(12, addr[2])
        self.assertEqual(121, addr[3])
        self.assertTrue(IPv4Address.is_private(addr))
        self.assertEqual(8080, v4addr.port)

        addr = IPv4Address("127.255.0.4", 8080).nbo_host
        self.assertFalse(IPv4Address.is_private(addr))
        addr = IPv4Address("128.1.0.4", 8080).nbo_host
        self.assertFalse(IPv4Address.is_private(addr))

        # Web server running in 172.16/12
        v4addr = IPv4Address("172.30.0.1", 443)
        addr = v4addr.nbo_host
        self.assertEqual(172, addr[0])
        self.assertEqual(30, addr[1])
        self.assertEqual(0, addr[2])
        self.assertEqual(1, addr[3])
        self.assertTrue(IPv4Address.is_private(addr))
        self.assertEqual(443, v4addr.port)

        addr = IPv4Address("172.15.0.1", 443).nbo_host
        self.assertFalse(IPv4Address.is_private(addr))
        addr = IPv4Address("172.32.0.1", 443).nbo_host
        self.assertFalse(IPv4Address.is_private(addr))

    def test_rfc3330(self):

        test = bytearray([0, 0, 0, 1])     # gets modified
        # 0/8
        self.assertTrue(IPv4Address.is_rfc3330(test))
        self.assertTrue(IPv4Address.is_rfc3330_not_private(test))
        # 14/8
        test[0] = 14
        self.assertTrue(IPv4Address.is_rfc3330(test))
        # 24/8
        test[0] = 24
        self.assertTrue(IPv4Address.is_rfc3330(test))
        # 127/0
        test[0] = 127
        self.assertTrue(IPv4Address.is_rfc3330(test))

        # 169.254/16, link local
        test = IPv4Address("169.254.0.1", 443).nbo_host
        self.assertEqual(169, test[0])
        self.assertEqual(254, test[1])
        self.assertTrue(IPv4Address.is_rfc3330(test))
        self.assertFalse(IPv4Address.is_private(test))

        # 192.0.2.0/24, test net
        test = IPv4Address("192.0.2.14", 443).nbo_host
        self.assertEqual(192, test[0])
        self.assertTrue(IPv4Address.is_rfc3330(test))
        self.assertFalse(IPv4Address.is_private(test))

        # 192.88.99.0/24, 6to4 relay anycast
        test = IPv4Address("192.88.99.14", 443).nbo_host
        self.assertEqual(192, test[0])
        self.assertTrue(IPv4Address.is_rfc3330(test))

        # 198.18/15, benchmark testing
        test = IPv4Address("198.18.99.14", 443).nbo_host
        self.assertEqual(198, test[0])
        self.assertTrue(IPv4Address.is_rfc3330(test))
        test = IPv4Address("198.19.99.14", 443).nbo_host
        self.assertTrue(IPv4Address.is_rfc3330(test))

        # 224/4, multicast
        test = IPv4Address("224.18.99.14", 443).nbo_host
        self.assertEqual(224, test[0])
        self.assertTrue(IPv4Address.is_rfc3330(test))

        # 240/4, reserved
        v4addr = IPv4Address("240.18.99.14", 443)
        test = v4addr.nbo_host
        self.assertEqual(240, test[0])
        self.assertTrue(IPv4Address.is_rfc3330(test))
        self.assertEqual("240.18.99.14:443", v4addr.__str__())

    # XXX DNS LOOKUP NOT YET SUPPORTED
#   def test_constructor_with_host_name(self):
#       v4addr = IPv4Address("www.xlattice.org", 80)
#       test = v4addr.nbo_host
#       # known to be globally routable ;-)
#       self.assertFalse(IPv4Address.is_rfc3330(test))


if __name__ == '__main__':
    unittest.main()
