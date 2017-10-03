import os
import sys

thisDirPath = os.path.dirname( os.path.abspath( __file__ ) )
uberPath = os.path.join( thisDirPath, '..' )
if uberPath not in sys.path:
    sys.path.append( uberPath )
import unittest

from uberNode import UberNode, ValueWrapper


class Variable( UberNode ):
    
    def __init__( self, value, **kwargs ):
        UberNode.__init__( self, **kwargs )

        self.outputs['value'] = ValueWrapper( value )


class Add( UberNode ):
    
    def evaluate( self ):
        a = self.getInputValue( 'input1' )
        b = self.getInputValue( 'input2' )
        return a + b


class TestStringMethods( unittest.TestCase ):

    def test_parent( self ):
        parent = UberNode()
        child = UberNode()
        child.setParent( parent )
        self.assertTrue( child.parent == parent and child in parent.children )

    def test_reparent( self ):
        parent1 = UberNode()
        parent2 = UberNode()
        child = UberNode()
        child.setParent( parent1 )
        child.setParent( parent2 )
        self.assertTrue( child.parent == parent2 and child in parent2.children and child.parent != parent1 and child not in parent1.children )

    def test_connect( self ):
        input1 = Variable( 1 )
        input2 = Variable( 2 )
        add = Add()
        add.inputs['input1'] = input1.outputs['value']
        add.inputs['input2'] = input2.outputs['value']
        self.assertTrue( add.evaluate() == 3 )


if __name__ == '__main__':
    unittest.main()