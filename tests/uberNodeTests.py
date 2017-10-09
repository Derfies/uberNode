import os
import sys

thisDirPath = os.path.dirname( os.path.abspath( __file__ ) )
uberPath = os.path.join( thisDirPath, '..' )
if uberPath not in sys.path:
    sys.path.append( uberPath )
import unittest

from uberNode import UberNode


class Variable( UberNode ):
    
    def __init__( self, value, **kwargs ):
        UberNode.__init__( self, **kwargs )

        self.addOutput( 'value', value )


class Link( UberNode ):

    def __init__( self, **kwargs ):
        UberNode.__init__( self, **kwargs )

        self.addInput( 'in' )
        self.addOutput( 'out' )

    def evaluate( self, **inputs ):
        return {'out': inputs['in']}


class Add( UberNode ):

    def __init__( self, **kwargs ):
        UberNode.__init__( self, **kwargs )

        self.addInput( 'a' )
        self.addInput( 'b' )
        self.addOutput( 'result' )
    
    def evaluate( self, **inputs ):
        return {
            'result': inputs['a'] + inputs['b']
        }


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

    def test_outputValue( self ):
        self.assertTrue( Variable( 1 ).getOutputValue() == 1 )

    def test_oneConnection( self ):
        var = Variable( 1 )
        lnk = Link()
        var.connect( 'value', lnk, 'in' )
        self.assertTrue( lnk.getOutputValue() == 1 )

    def test_oneConnectionChangeValue( self ):
        var = Variable( 1 )
        lnk = Link()
        var.connect( 'value', lnk, 'in' )
        var.setOutputValue( 'value', 2 )
        self.assertTrue( lnk.getOutputValue() == 2 )

    def test_twoConnections( self ):
        var = Variable( 1 )
        lnk1 = Link()
        lnk2 = Link()
        var.connect( 'value', lnk1, 'in' )
        lnk1.connect( 'out', lnk2, 'in' )
        self.assertTrue( lnk2.getOutputValue() == 1 )

    def test_twoConnectionsChangeValue( self ):
        var = Variable( 1 )
        lnk1 = Link()
        lnk2 = Link()
        var.connect( 'value', lnk1, 'in' )
        lnk1.connect( 'out', lnk2, 'in' )
        var.setOutputValue( 'value', 2 )
        self.assertTrue( lnk2.getOutputValue() == 2 )

    def test_basicGraph( self ):
        var1 = Variable( 1 )
        var2 = Variable( 2 )
        add = Add()
        var1.connect( 'value', add, 'a' )
        var2.connect( 'value', add, 'b' )
        self.assertTrue( add.getOutputValue() == 3 )

    # def test_reconnect( self ):
    #     var1 = Variable( 1 )
    #     var2 = Variable( 2 )
    #     var3 = Variable( 3 )
    #     add = Add()
    #     add.inputs['a'] = var1.outputs['value']
    #     add.inputs['b'] = var2.outputs['value']
    #     add.evaluate()
    #     oldValue = add.getOutputValue()
    #     add.inputs['b'] = var3.outputs['value']
    #     add.evaluate()
    #     newValue = add.getOutputValue()
    #     self.assertTrue( oldValue == 3 and newValue == 4 )

    # def test_basicGraph( self ):

    #     # Add 2 and 1.
    #     var1 = Variable( 1 )
    #     var2 = Variable( 2 )
    #     add1 = Add()
    #     add1.inputs['a'] = var1.outputs['value']
    #     add1.inputs['b'] = var2.outputs['value']
    #     add1.evaluate()

    #     # Add the result to 3.
    #     var3 = Variable( 3 )
    #     add2 = Add()
    #     add2.inputs['a'] = add1.outputs['result']
    #     add2.inputs['b'] = var3.outputs['value']
    #     add2.evaluate()

    #     self.assertTrue( add1.getOutputValue() == 3 and add2.getOutputValue() == 6 )


if __name__ == '__main__':
    unittest.main()