__all__ = [
    "FALSEY_UNDEFINED",
    "STRINGABLE_FALSEY_UNDEFINED",
    "STRINGABLE_UNDEFINED",
    "UNDEFINED",
    "AllowedAttribute",
    "Undefined",
    "is_undefined",
]

import dataclasses
from collections.abc import Callable, Collection
from typing import Any, ClassVar, Final, NoReturn, Self, TypeIs, final


@dataclasses.dataclass(frozen=True, slots=True)
class AllowedAttribute:
    """
    Data class to store information describing allowed attribute for the Undefined class.

    Parameters:
        attribute (str): The name of the attribute to allow access. Required.
        callback (Callable[..., Any]): The callback to call on access to the attribute. Required.
            Ensure that the callback repeats interface of the target method.
        alias (str | None): The alias for the attribute. Optional. Useful for scenarios when you want to
            provide several undefined objects with the same allowed arguments but different attributes.
    """

    attribute: str
    callback: Callable[..., Any]
    alias: str | None = None


_ALWAYS_ALLOWED_ATTRIBUTES: tuple[str, ...] = (
    "_Undefined__allowed_attributes",
    "__init__",
    "__class__",
)
"""
Collection of attributes that are always allowed for the Undefined class.

Attributes in this collection are required for the internal implementation, and access to them is always allowed.
They are moved outside of the Undefined class to avoid recursion in the __getattribute__ method.
"""


class Undefined:
    """
    A class to represent an undefined value.

    Useful for scenarios where value will be defined later, but you need to define a variable on the initialization
    stage. For example, you want to define existing of some lazy entity, but you don't want to fetch it without a need.

    This class is not a singleton, but restrict the number of instances to one per parameter set based on the exact
    usage of it. In the most strict case, this class will raise an attribute error on any attempt to access properties
    of the instance.

    Note:
        Python has different behaviour between calling of the magic methods and access to them using built-in functions.
        Basic implementation of this class guarantees correct behaviour for calling `__str__`, `__bool__`,
        and `__repr__` based on specified configuration.

        If you need to implement similar behaviour for another build-in calls, you need explicitly inherit
        from this class and override the necessary methods.

        See details: https://docs.python.org/3/reference/datamodel.html#special-method-lookup

    Parameters:
            allowed_attributes (Collection[AllowedAttribute]): The list of allowed arguments for the instance.
            For items in the list, the access to the attribute will be allowed. If None, only the `__init__`
            and `_Undefined__allowed_attributes` are allowed for proper work of the class.
    """

    __instances: ClassVar[dict[frozenset[str], Self]] = {}

    @final
    def __new__(cls, *allowed_attributes: AllowedAttribute) -> Self:
        """
        Return the same instance of the class per each set of allowed arguments.

        Parameters:
            allowed_attributes (Collection[AllowedAttribute]): The list of allowed attributes for
            the instance. It may be an attribute name, or a tuple with the attribute name and the callback to call.

        Returns:
            Self: The instance of the class with the defined callbacks for the allowed attributes.

        """
        instance_identifier = cls.__to_instance_identifier(allowed_attributes)
        if instance_identifier not in cls.__instances:
            instance = super().__new__(cls)
            # __new__ and __init__ methods are final and must be compatible
            # The only reason class itself is not final it a need of inheritance for the possible built-in methods
            # workaround
            instance.__init__(*allowed_attributes)  # type: ignore[misc]
            cls.__instances[instance_identifier] = instance

        return cls.__instances[instance_identifier]

    @final
    def __init__(self, *allowed_attributes: AllowedAttribute) -> None:
        self.__allowed_attributes: dict[str, Callable[..., Any]] = {}
        for item in allowed_attributes:
            setattr(self, item.attribute, item.callback)
            self.__allowed_attributes[item.attribute] = item.callback

    def __str__(self) -> str:
        """
        Override of the __str__ method to return the default message for the Undefined object.

        Returns:
            str: Default message for Undefined object.

        Raises:
            ValueError: If the access to the attribute is restricted.
            AssertionError: If method returns a value of the wrong type.
        """
        if "__str__" in self.__allowed_attributes:
            return Undefined.__validate_correct_type(self.__allowed_attributes["__str__"](), str)
        Undefined.__raise_access_error("__str__")

    def __repr__(self) -> str:
        """
        Override of the __repr__ method to return the default message for the Undefined object.

        Returns:
            str: Default message for Undefined object.

        Raises:
            ValueError: If the access to the attribute is restricted.
            AssertionError: If method returns a value of the wrong type.
        """
        if "__repr__" in self.__allowed_attributes:
            return Undefined.__validate_correct_type(self.__allowed_attributes["__repr__"](), str)
        Undefined.__raise_access_error("__repr__")

    def __bool__(self) -> bool:
        """
        Override of the __bool__ method to always return False.

        Returns:
            bool: Default value for the Undefined object.

        Raises:
            ValueError: If the access to the attribute is restricted.
            AssertionError: If method returns a value of the wrong type.
        """
        if "__bool__" in self.__allowed_attributes:
            return Undefined.__validate_correct_type(self.__allowed_attributes["__bool__"](), bool)
        Undefined.__raise_access_error("__bool__")

    def __getattribute__(self, item: str) -> Any:  # noqa: ANN401 - Any is useful here
        """
        Override of the __getattribute__ method to raise an error on any access to the instance properties.

        Arguments:
            item (str): The name of the attribute to access.

        Raises:
            ValueError: Always, as the access to the attribute is restricted. Exception made for several methods,
            such as __str__, __bool__, and __repr__, if they are allowed for the instance.

        Returns:
            Any: The value of the attribute if it is allowed for the instance.
        """
        if item in _ALWAYS_ALLOWED_ATTRIBUTES or item in self.__allowed_attributes:
            return super().__getattribute__(item)
        Undefined.__raise_access_error(item)

    @staticmethod
    def __raise_access_error(item: str) -> NoReturn:
        msg = (
            f"[UNDEFINED] You are referencing undefined object. Access to the attribute {item!r} is impossible. "
            f"Ensure you populate the value before using any of its properties."
        )
        raise ValueError(msg)

    @staticmethod
    def __validate_correct_type[T](result: Any, expected_type: type[T]) -> T:  # noqa: ANN401 - Any is useful here
        if not isinstance(result, expected_type):
            msg = f"The __str__ method must return a string, got {type(result)} instead."
            raise AssertionError(msg)  # noqa: TRY004 - It's a developer mistake, not a code error
        return result

    @classmethod
    def __to_instance_identifier(cls, allowed_attributes: Collection[AllowedAttribute] = ()) -> frozenset[str]:
        result = set()
        for attribute in allowed_attributes:
            if attribute.attribute in _ALWAYS_ALLOWED_ATTRIBUTES:
                msg = f"Attribute {attribute!r} is reserved for the internal use."
                raise ValueError(msg)
            if attribute.attribute in result:
                msg = f"Duplicate argument {attribute.attribute!r} in the allowed arguments."
                raise ValueError(msg)
            result |= {f"{attribute.attribute}|{attribute.alias}" if attribute.alias else attribute.attribute}
        return frozenset(result)


UNDEFINED: Final[Any] = Undefined()
STRINGABLE_UNDEFINED: Final[Any] = Undefined(
    AllowedAttribute("__str__", lambda: "[UNDEFINED]"),
    AllowedAttribute("__repr__", lambda: "[UNDEFINED]"),
)
FALSEY_UNDEFINED: Final[Any] = Undefined(AllowedAttribute("__bool__", lambda: False))
STRINGABLE_FALSEY_UNDEFINED: Final[Any] = Undefined(
    AllowedAttribute("__str__", lambda: "[UNDEFINED]"),
    AllowedAttribute("__repr__", lambda: "[UNDEFINED]"),
    AllowedAttribute("__bool__", lambda: False),
)


def is_undefined(value: Any) -> TypeIs[Undefined]:  # noqa: ANN401 - Any is useful here
    """
    Check if the value is an undefined value.

    Arguments:
        value (Any): The value to check.

    Returns:
        bool: True if the value is an undefined value, False otherwise.
    """
    return isinstance(value, Undefined)
