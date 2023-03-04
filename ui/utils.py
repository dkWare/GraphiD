from .debugger import logger as dbg
from .debugger import Tag as _debugger_tags


class _BetterLog:
    def __str__(self) -> str:
        key_pairs:list[tuple[str, float]] = [(key, value) for key, value in vars(self).items()]
        keyargs_list:list[str] = []
        for pair in key_pairs:
            if pair[1] is None:
                continue
            keyarg = str(pair[0]).removeprefix("_")+'='+str(pair[1]).removeprefix("_")
            keyargs_list.append(keyarg)
        return f"{type(self).__name__}({', '.join(keyargs_list)})"


class Vector2D(_BetterLog):
    def __init__(self, a: float, b: float, id:str=None):
        """
        This Class represents a simple two dimensional Vector
        It has two values:

        - a: float | int
        - b: float | int

        ## properties
        you can get the values separate by using:
        - @valA for the content of a
        - @valB for the content of b
        or both in a tuple by using:
        - @values
        """
        self._a = a
        self._b = b
        self._id = id
        dbg.debug(f"created Vector2D {self}", extra={"tags": [_debugger_tags.MU_VECTOR_HANDLING, _debugger_tags.M_UTILS], 'classname': self.__class__.__name__})

    def __add__(self, other: tuple):
        self._a += other[0]
        self._b += other[1]
        return self

    @property
    def valA(self):
        return self._a

    @property
    def valB(self):
        return self._b

    @property
    def values(self):
        return self._a, self._b


class MousePointer(Vector2D):
    """
    This Class represents the position off the Mouse
    It has two values:

     - a: float | int
     - b: float | int

    ## properties
    you can get the values separate by using:
     - @valA for the content of a
     - @valB for the content of b
    or both in a tuple by using:
     - @values
    ## methods
    you can use the change method to change a and b:
     - @change(new_a: float|int, new_b: float|int)
    """
    def __init__(self, a: float, b: float, id:str=None):
        super().__init__(a, b, id)

    def change(self, a, b):
        self._a = a
        self._b = b