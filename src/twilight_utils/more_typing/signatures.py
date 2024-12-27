from collections.abc import Callable
from inspect import get_annotations
from typing import Any


def has_same_signature(
    to_compare: Callable[..., Any],
    compare_with: Callable[..., Any],
    *,
    compare_names: bool = False,
    locals_: dict[str, Any] | None = None,
    globals_: dict[str, Any] | None = None,
) -> bool:
    """
    Check that two functions have the same signature.

    NOTE: This function does not check the implementation of the functions, as well as their real compatibility.
    It only checks that interfaces of the two functions are the same according to their annotations.

    Args:
        to_compare (Callable[..., Any]): Function to compare.
        compare_with (Callable[..., Any]): Function to compare with.
        compare_names (bool): Whether to compare the names of the functions. Defaults to False.
        locals_ (dict[str, Any]): Local variables to use for the comparison. Defaults to None. Should repeat
            the functionality of the `locals` parameters of `inspect.get_annotations`.
        globals_ (dict[str, Any]): Global variables to use for the comparison. Defaults to None. Should repeat
            the functionality of the `globals` parameters of `inspect.get_annotations`.

    Returns:
        bool: True if the functions have the same signature, False otherwise.
    """
    to_compare_annotations = get_annotations(to_compare, locals=locals_, globals=globals_, eval_str=True)
    compare_with_annotations = get_annotations(compare_with, locals=locals_, globals=globals_, eval_str=True)
    if len(to_compare_annotations) != len(compare_with_annotations):
        return False

    for to_compare_annotation, compare_with_annotation in zip(
        to_compare_annotations, compare_with_annotations, strict=True
    ):
        if compare_names and to_compare_annotation != compare_with_annotation:
            return False

        if to_compare_annotations[to_compare_annotation] != compare_with_annotations[compare_with_annotation]:
            return False

    return True
