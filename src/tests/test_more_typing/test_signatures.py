import unittest

from std_utils.more_typing.signatures import has_same_signature


def _func_a(x: int, y: str) -> None:
    pass


def _func_b(x: int, y: str) -> None:
    pass


def _func_c(x: int, y: int) -> None:
    pass


def _func_d(x: int, y: str, z: float) -> None:
    pass


def _func_e(x: int, z: str) -> None:
    pass


class TestHasSameSignature(unittest.TestCase):
    """Test that the has_same_signature function works as expected."""

    def test_functions_with_same_signature(self) -> None:
        """Check that two functions with the same signature are considered to have the same signature."""
        self.assertTrue(has_same_signature(_func_a, _func_b))

    def test_functions_with_different_signature(self) -> None:
        """Check that two functions with different types are considered to have different signatures."""
        self.assertFalse(has_same_signature(_func_a, _func_c))

    def test_functions_with_different_number_of_parameters(self) -> None:
        """Check that two functions with different number of parameters are considered to have different signatures."""
        self.assertFalse(has_same_signature(_func_a, _func_d))

    def test_functions_with_same_signature_and_names(self) -> None:
        """
        Check that two functions with the same types and different names are considered to have the same signature in
        case the names are not compared.
        """  # noqa: D205
        self.assertTrue(has_same_signature(_func_a, _func_e, compare_names=False))

    def test_functions_with_different_names(self) -> None:
        """
        Check that two functions with the same types and different names are considered to have different signatures in
        case the names are compared.
        """  # noqa: D205
        self.assertFalse(has_same_signature(_func_a, _func_e, compare_names=True))
