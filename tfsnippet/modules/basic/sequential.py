import tensorflow as tf

from .base import Module

__all__ = ['Sequential']


class Sequential(Module):
    """
    Wrapping a sequential of neural network modules as a :class:`Module`.

    This class wraps a sequential of neural network layers (or modules)
    into a unified :class:`Module`, reusing the parameters inside each
    component.  Instances of :class:`Module` and any arbitrary function
    can be mixed together freely.  For example:

    .. code-block:: python

        from tensorflow.contrib import layers
        from tfsnippet.modules import Dense, Linear

        mlp = Sequential([
            lambda inputs: layers.fully_connected(
                inputs, num_outputs=100, activation_fn=tf.nn.relu),
            Dense(100, activation_fn=tf.nn.relu),
            Linear(1),
            tf.nn.sigmoid
        ])

    Which builds a multi-layer perceptron, with 2 hidden layers of 100
    units and ReLU activation, plus a sigmoid output layer with 1 unit.

    .. note::
        If another instance of :class:`Module` is specified as one component,
        the variables of that module is managed within its own scope, instead
        of the scope of this sequential module.
        On the other hand, if instead a function or a method is provided, it
        will be called within a child scope of this :class:`Sequential` module.

        As a result, in the above code example, the parameters of the first
        hidden layer (derived by :func:`~tf.contrib.layers.fully_connected`)
        would be collected in the scope ``sequential/_0/``, while the
        parameters of the second hidden layer (derived by an instance of
        :class:`~tfsnippet.modules.Dense`) would be collected in the scope
        ``dense/``, which is the scope of the dense module itself.

    Args:
        components (list[(inputs, \**kwargs) -> outputs]):
            Components of this sequential module, each should be a callable
            object which consumes the outputs of previous component as inputs.

            The first component should consume the `inputs` as well as the
            named arguments (`\**kwargs`) given to the whole :class:`Sequential`
            module.  The outputs of the last component will be the outputs of
            the whole :class:`Sequential` module.

        name (str): Optional name of this module
                    (argument of :class:`~tfsippet.scaffold.VarScopeObject`).
        scope (str): Optional scope of this module
                    (argument of :class:`~tfsippet.scaffold.VarScopeObject`).
    """

    def __init__(self, components, name=None, scope=None):
        components = tuple(components)
        if not components:
            raise ValueError('`components` must not be empty')
        super(Sequential, self).__init__(name=name, scope=scope)
        self._components = components

    def _forward(self, inputs, **kwargs):
        outputs = inputs
        for i, c in enumerate(self._components):
            with tf.variable_scope('_%d' % i):
                if i == 0:
                    outputs = c(outputs, **kwargs)
                else:
                    outputs = c(outputs)
        return outputs
