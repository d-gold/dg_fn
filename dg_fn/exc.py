class NotCadrExpressionError(Exception):

    """Docstring for NotCadrExpressionError. """

    def __init__(self, name):
        """@todo: to be defined1.

        :name: @todo

        """
        self._name = name
        Exception.__init__(self, "{} is not a cadr expression".format(name))
