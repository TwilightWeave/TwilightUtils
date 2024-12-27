from unittest import TestCase

from twilight_utils.more_typing.undefined import (
    FALSEY_UNDEFINED,
    STRINGABLE_FALSEY_UNDEFINED,
    STRINGABLE_UNDEFINED,
    UNDEFINED,
    AllowedAttribute,
    Undefined,
)


class UndefinedTestCase(TestCase):
    """Test that the behaviour of the undefined class working as expected."""

    def test_undefined_is_indeed_singleton(self) -> None:
        """Ensure that the undefined class is indeed a singleton."""
        undefined = Undefined()
        undefined_str = Undefined(
            AllowedAttribute("__str__", lambda: "[UNDEFINED]"),
            AllowedAttribute("__repr__", lambda: "[UNDEFINED]"),
        )
        undefined_bool = Undefined(AllowedAttribute("__bool__", lambda: False))
        undefined_both = Undefined(
            AllowedAttribute("__str__", lambda: "[UNDEFINED]"),
            AllowedAttribute("__repr__", lambda: "[UNDEFINED]"),
            AllowedAttribute("__bool__", lambda: False),
        )
        undefined_truth_bool = Undefined(AllowedAttribute("__bool__", lambda: True, alias="truth"))
        self.assertIs(undefined, UNDEFINED)
        self.assertIs(undefined_str, STRINGABLE_UNDEFINED)
        self.assertIs(undefined_bool, FALSEY_UNDEFINED)
        self.assertIs(undefined_both, STRINGABLE_FALSEY_UNDEFINED)
        self.assertIsNot(undefined_truth_bool, FALSEY_UNDEFINED)

    def test_undefined_raise_error_on_any_attribute_access(self) -> None:
        """Ensure that the undefined class raises an error on any attribute access."""
        self._asert_arbitrary_property_raises()
        with self.assertRaises(ValueError):
            _ = bool(UNDEFINED)
        with self.assertRaises(ValueError):
            _ = UNDEFINED.__bool__()  # noqa: PLC2801 - Testing direct __bool__ call
        with self.assertRaises(ValueError):
            _ = str(UNDEFINED)
        with self.assertRaises(ValueError):
            _ = UNDEFINED.__str__()  # noqa: PLC2801 - Testing direct __str__ call
        with self.assertRaises(ValueError):
            _ = repr(UNDEFINED)
        with self.assertRaises(ValueError):
            _ = UNDEFINED.__repr__()  # noqa: PLC2801 - Testing direct __repr__ call

    def test_undefined_str_correctly_raises_errors(self) -> None:
        """Ensure that the undefined class raises an error on non-stringable access."""
        self._asert_arbitrary_property_raises()
        with self.assertRaises(ValueError):
            _ = bool(STRINGABLE_UNDEFINED)
        with self.assertRaises(ValueError):
            _ = STRINGABLE_UNDEFINED.__bool__()  # noqa: PLC2801 - Testing direct __bool__ call
        self.assertEqual(str(STRINGABLE_UNDEFINED), "[UNDEFINED]")
        self.assertEqual(STRINGABLE_UNDEFINED.__str__(), "[UNDEFINED]")  # noqa: PLC2801 - Testing direct __str__ call
        self.assertEqual(repr(STRINGABLE_UNDEFINED), "[UNDEFINED]")
        self.assertEqual(STRINGABLE_UNDEFINED.__repr__(), "[UNDEFINED]")  # noqa: PLC2801 - Testing direct __repr__ call

    def test_undefined_bool_correctly_raises_errors(self) -> None:
        """Ensure that the undefined class raises an error on non-falsable access."""
        self._asert_arbitrary_property_raises()
        with self.assertRaises(ValueError):
            _ = str(FALSEY_UNDEFINED)
        with self.assertRaises(ValueError):
            _ = FALSEY_UNDEFINED.__str__()  # noqa: PLC2801 - Testing direct __str__ call
        with self.assertRaises(ValueError):
            _ = repr(FALSEY_UNDEFINED)
        with self.assertRaises(ValueError):
            _ = FALSEY_UNDEFINED.__repr__()  # noqa: PLC2801 - Testing direct __repr__ call
        self.assertFalse(bool(FALSEY_UNDEFINED))
        self.assertFalse(FALSEY_UNDEFINED.__bool__())  # noqa: PLC2801 - Testing direct __bool__ call

    def test_undefined_str_bool_correctly_raises_errors(self) -> None:
        """Ensure that the undefined class raises an error on non-stringable and non-falsable access."""
        self._asert_arbitrary_property_raises()
        self.assertEqual(str(STRINGABLE_FALSEY_UNDEFINED), "[UNDEFINED]")
        self.assertEqual(STRINGABLE_FALSEY_UNDEFINED.__str__(), "[UNDEFINED]")  # noqa: PLC2801 - Testing direct __str__ call
        self.assertFalse(bool(STRINGABLE_FALSEY_UNDEFINED))
        self.assertFalse(STRINGABLE_FALSEY_UNDEFINED.__bool__())  # noqa: PLC2801 - Testing direct __bool__ call
        self.assertEqual(repr(STRINGABLE_FALSEY_UNDEFINED), "[UNDEFINED]")
        self.assertEqual(STRINGABLE_FALSEY_UNDEFINED.__repr__(), "[UNDEFINED]")  # noqa: PLC2801 - Testing direct __repr__ call

    def test_custom_undefined_returns_expected_values(self) -> None:
        """Ensure that the custom undefined class returns the expected values."""
        undefined_custom = Undefined(
            AllowedAttribute("__str__", lambda: "Custom undefined"),
            AllowedAttribute("custom_function", lambda: "Custom undefined"),
        )
        self.assertEqual(str(undefined_custom), "Custom undefined")
        self.assertEqual(undefined_custom.__str__(), "Custom undefined")  # noqa: PLC2801 - Testing direct __str__ call
        self.assertEqual(undefined_custom.custom_function(), "Custom undefined")

    def _asert_arbitrary_property_raises(self) -> None:
        with self.assertRaises(ValueError):
            _ = STRINGABLE_FALSEY_UNDEFINED.some_attribute
        with self.assertRaises(ValueError):
            _ = STRINGABLE_FALSEY_UNDEFINED.some_method()
        with self.assertRaises(ValueError):
            _ = STRINGABLE_FALSEY_UNDEFINED.some_property
