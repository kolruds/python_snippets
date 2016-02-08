class Decorate_Class(object):
    _mxs_val = 0
    def __init__(self, value):
        self._original = value


# Trivial example. Simulate a MaxScript variable with a class variable.
# Initialize two instances with different values.
test_1 = Decorate_Class(10)
Decorate_Class._mxs_val = 10 # Just to simulate.

print 'test_1 has attributes: _mxs_val: %s, _original: %s' % (
    test_1.__class__._mxs_val, test_1._original)

# >>> test_1 has attributes: _mxs_val: 10, _original: 10

test_2 = Decorate_Class(20)
Decorate_Class._mxs_val = 20 # Just to simulate

print 'test_2 has attributes: _mxs_val: %s, _original: %s' % (
    test_2.__class__._mxs_val, test_2._original)

# >>> test_2 has attributes: _mxs_val: 20, _original: 20

# We have now initialized two instances. Each can have their own variables with
# useful information, but the reference back to MaxScript will always point to
# the newest we initialized. Lets check that:
print "test_1 will point to MaxScript variable %s, but was originally %s" % (
    test_1.__class__._mxs_val, test_1._original) 

# >>> test_1 will point to MaxScript variable 20, but was originally 10

# With a decorator, we can always ensure maxscript is pointing to the right value:

class Decorate_Class_2(object):
    _mxs_val = 0
    def __init__(self, value):
        self._original = value
    
    def update_mxs(fn):
        def wrapper(*args, **kwargs):
            print 'Decorated to update MaxScript value before running'
            print '_mxs_val is %s, will be set to _original; %s' % (
                args[0].__class__._mxs_val, args[0]._original)
            args[0].__class__._mxs_val = args[0]._original
            return fn(*args, **kwargs)
        return wrapper

    @update_mxs
    def test_function(self):
        print 'Function called in instance.'


# Initialize a third test with the a decorated function, and call it:
test_3 = Decorate_Class_2(30)
test_3.test_function()

# Output the class and instance variables:
print 'test_3 has attributes: _mxs_val: %s, _original: %s' % (
    test_3.__class__._mxs_val, test_3._original)

# Here, we did not "simulate" the mxs var in the same way, this should happen
# automatically. Here is the output:

# >>> Decorated to update MaxScript value before running
# >>> _mxs_val is 0, will be set to _original; 30
# >>> Function called in instance.
# >>> test_3 has attributes: _mxs_val: 30, _original: 30

# This sould be implemented as class variables as shown here, so that the
# decorator can check the class variable before changing the MaxScript variable.
# The decorator should then be applied to all functions that has direct contact
# to the maxscript variable.
