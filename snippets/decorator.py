"""
Classic implementation of the Decorator pattern as defined in GOF.

Attach additional responsibilities to an object dynamically Decorators
provide a flexible alternative to subclassing for extending functionality.
"""

class Component(object):
    def __init__(self):
        pass

    def draw(self):
        print "draw"
    
    def resize(self):
        print "resize"


class Decorator(Component):
    def __init__(self, component):
        self._component = Component

    def draw(self):
        self._component.draw()

    def resize(self):
        self._component.resize()


class FooDecorator(Decorator):
    def __init__(self, component, foo_count):
        self._component = component
        self.count = foo_count

    def draw_foo(self):
        print 'foo'*self.count

    def draw(self):
        self._component.draw()
        self.draw_foo()

class BarDecorator(Decorator):
    def __init__(self, component, bar_count):
        self._component = component
        self.count = bar_count

    def draw_bar(self):
        print 'bar'*self.count

    def draw(self):
        self._component.draw()
        self.draw_bar()


def main():
    obj = FooDecorator(BarDecorator(Component(),2),1)
    obj.draw()
    obj.resize()

if __name__ == '__main__':
    main()

