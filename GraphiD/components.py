from typing import overload


class MetaVector(type):
    def __new__(cls, name, bases, attrs):
        new_cls = super().__new__(cls, name, bases, attrs)
        new_cls._init()
        return new_cls

    @property
    def zero(cls):
        return cls.copy(cls._zero)

    @property
    def up(cls):
        return cls.copy(cls._up)

    @property
    def down(cls):
        return cls.copy(cls._down)

    @property
    def left(cls):
        return cls.copy(cls._left)

    @property
    def right(cls):
        return cls.copy(cls._right)


class Vector2D(metaclass=MetaVector):
    _zero = None
    _up = None
    _down = None
    _left = None
    _right = None

    @classmethod
    def _init(cls):
        cls._zero = cls(0, 0, "ZeroVector2D")
        cls._up = cls(0, 1, "UpVector2D")
        cls._down = cls(0, -1, "DownVector2D")
        cls._left = cls(-1, 0, "LeftVector2D")
        cls._right = cls(1, 0, "RightVector2D")

    @classmethod
    def copy(cls, other, new_id=None):
        return cls(*other.values, id=new_id)

    def __init__(self, a: float, b: float, id: str=None):
        self.__a = a
        self.__b = b

        self.__id = id

    def _change_values(self, new_a: float, new_b: float):
        self.__a = new_a
        self.__b = new_b

    def _change_rel(self, da: float, db: float):
        self.__a += da
        self.__b += db

    @overload
    def _change_rel(self, delta_position):
        self.__a += delta_position.valA
        self.__b += delta_position.valB

    @property
    def ID(self):
        return self.__id

    @property
    def valA(self):
        return self.__a

    @property
    def valB(self):
        return self.__b

    @property
    def values(self):
        return self.__a, self.__b


class Vector3D(Vector2D):
    def __init__(self, a: float, b: float, c: float, id: str=None):
        super().__init__(a, b, id)
        self.__c = c

    @property
    def valC(self):
        return self.__c

    @property
    def values(self):
        return self.valA, self.valB, self.__c


class Transform:
    def __init__(self, position: Vector2D=Vector2D.zero, id: str=None):
        self.__position = position
        self.__id = id

    def __add__(self, x):
        if isinstance(x, Vector2D):
            return Vector2D(self.__position.valA + x.valA,
                            self.__position.valB + x.valB)
        return Vector2D(self.__position.valA + x,
                        self.__position.valB + x)
    def __sub__(self, x):
        if isinstance(x, Vector2D):
            return Vector2D(self.__position.valA - x.valA,
                            self.__position.valB - x.valB)
        return Vector2D(self.__position.valA - x,
                        self.__position.valB - x)
    def __mul__(self, x):
        if isinstance(x, Vector2D):
            return Vector2D(self.__position.valA * x.valA,
                            self.__position.valB * x.valB)
        return Vector2D(self.__position.valA * x,
                        self.__position.valB * x)
    def __truediv__(self, x):
        if isinstance(x, Vector2D):
            return Vector2D(self.__position.valA / x.valA,
                            self.__position.valB / x.valB)
        return Vector2D(self.__position.valA / x,
                        self.__position.valB / x)
    def __floordiv__(self, x):
        if isinstance(x, Vector2D):
            return Vector2D(self.__position.valA // x.valA,
                            self.__position.valB // x.valB)
        return Vector2D(self.__position.valA // x,
                        self.__position.valB // x)
    def __pow__(self, x: int):
        return Vector2D(self.__position.valA**x, self.__position.valB**x)
    def __iadd__(self, x):
        self.__position = self + x
        return self
    def __isub__(self, x):
        self.__position = self - x
        return self
    def __imul__(self, x):
        self.__position = self * x
        return self
    def __itruediv__(self, x):
        self.__position = self / x
        return self
    def __ifloordiv__(self, x):
        self.__position = self // x
        return self

    @property
    def ID(self):
        return self.__id

    @property
    def position(self):
        return self.__position.values

    @property
    def X(self):
        return self.__position.valA

    @property
    def Y(self):
        return self.__position.valA


class Body:
    def __init__(self, transform, size: Vector2D):
        ...


class ComponentHandler:
    def __init__(self, **components):
        self.__transform = components.get("transform", Transform)


    @property
    def TRANSFORM(self):
        return self.__transform