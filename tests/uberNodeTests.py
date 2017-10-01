import unittest

from uberNode import UberNode as Node


class TestStringMethods( unittest.TestCase ):

    def test_parent( self ):
        parent = Node()
        child = Node()
        child.setParent( parent )
        self.assertTrue( child.parent == parent and child in parent.children )


if __name__ == '__main__':
    unittest.main()