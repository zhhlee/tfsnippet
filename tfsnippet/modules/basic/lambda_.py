from tfsnippet.utils import docstring_inherit
from .base import Module

__all__ = ['Lambda']


class Lambda(Module):
    """
    Wrapping arbitrary function into a neural network :class:`Module`.

    This class wraps an arbitrary function or lambda expression into
    a neural network :class:`Module`, reusing the variables created
    within the specified function.

    For example, one may create a reusable fully connected layer
    module by using :class:`Lambda` component as follows:

    .. code-block:: python

        import functools
        from tensorflow.contrib import layers

        dense = Lambda(
            functools.partial(
                layers.fully_connected,
                num_outputs=100,
                activation_fn=tf.nn.relu
            )
        )

    Args:
        f ((inputs, \**kwargs) -> outputs): The function or lambda expression
                                               which derives the outputs.
        name (str): Optional name of this module
                    (argument of :class:`~tfsippet.scaffold.VarScopeObject`).
        scope (str): Optional scope of this module
                    (argument of :class:`~tfsippet.scaffold.VarScopeObject`).
    """

    def __init__(self, f, name=None, scope=None):
        super(Lambda, self).__init__(name=name, scope=scope)
        self._factory = f

    @docstring_inherit(Module._forward)
    def _forward(self, inputs, **kwargs):
        return self._factory(inputs, **kwargs)
