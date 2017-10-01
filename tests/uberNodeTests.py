import os
import sys

thisDirPath = os.path.dirname( os.path.abspath( __file__ ) )
uberPath = os.path.join( thisDirPath, '..' )
if uberPath not in sys.path:
	sys.path.append( uberPath )
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