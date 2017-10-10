import os
import sys

thisDirPath = os.path.dirname( os.path.abspath( __file__ ) )
uberPath = os.path.join( thisDirPath, '..' )
if uberPath not in sys.path:
    sys.path.append( uberPath )
import unittest

from uberNode import UberNode


class Input( UberNode ):
    
    def __init__( self, value, **kwargs ):
        UberNode.__init__( self, **kwargs )

        self.addOutput( 'value', value )


class Output( UberNode ):
    
    def __init__( self, **kwargs ):
        UberNode.__init__( self, **kwargs )

        self.addInput( 'value' )


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

    def test_addDuplicateInput( self ):
        node = UberNode()
        with self.assertRaises( Exception ) as context:
            node.addInput( 'foo' )
            node.addInput( 'foo' )
        self.assertTrue( 'Input "foo" already exists' in context.exception )

    def test_addDuplicateOutput( self ):
        node = UberNode()
        with self.assertRaises( Exception ) as context:
            node.addOutput( 'foo' )
            node.addOutput( 'foo' )
        self.assertTrue( 'Output "foo" already exists' in context.exception )

    def test_inputValue( self ):
        out = Output()
        in_ = Input( 1 )
        in_.connect( 'value', out, 'value' )
        self.assertTrue( out.getInputValue() == 1 )

    def test_inputValueChanged( self ):
        out = Output()
        in_ = Input( 1 )
        in_.connect( 'value', out, 'value' )
        oldVal = out.getInputValue()
        in_.setOutputValue( 'value', 2 )
        newVal = out.getInputValue()
        self.assertTrue( oldVal == 1 and newVal == 2 )

    def test_outputValue( self ):
        in_ = Input( 1 )
        self.assertTrue( in_.getOutputValue() == 1 )

    def test_outputValueChanged( self ):
        in_ = Input( 1 )
        oldVal = in_.getOutputValue()
        in_.setOutputValue( 'value', 2 )
        newVal = in_.getOutputValue()
        self.assertTrue( oldVal == 1 and newVal == 2 )

    def test_chain( self ):
        in_ = Input( 1 )
        lnk = Link()
        out = Output()
        in_.connect( 'value', lnk, 'in' )
        lnk.connect( 'out', out, 'value' )
        self.assertTrue( out.getInputValue() == 1 )

    # def test_twoConnectionsChangeValue( self ):
    #     var = Input( 1 )
    #     lnk1 = Link()
    #     lnk2 = Link()
    #     var.connect( 'value', lnk1, 'in' )
    #     lnk1.connect( 'out', lnk2, 'in' )
    #     var.setOutputValue( 'value', 2 )
    #     self.assertTrue( lnk2.getOutputValue() == 2 )

    def test_add( self ):
        var1 = Input( 1 )
        var2 = Input( 2 )
        add = Add()
        var1.connect( 'value', add, 'a' )
        var2.connect( 'value', add, 'b' )
        self.assertTrue( add.getOutputValue() == 3 )

    def test_addMore( self ):
        """Two inputs added together, then a third added after."""
        var1 = Input( 1 )
        var2 = Input( 2 )
        add1 = Add()
        var1.connect( 'value', add1, 'a' )
        var2.connect( 'value', add1, 'b' )
        var3 = Input( 3 )
        add2 = Add()
        add1.connect( 'result', add2, 'a' )
        var3.connect( 'value', add2, 'b' )
        self.assertTrue( add2.getOutputValue() == 6 )

    def test_recurse( self ):
        pass

    def test_disconnect( self ):
        pass



if __name__ == '__main__':
    unittest.main()