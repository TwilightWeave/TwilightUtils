import unittest
import uuid
from typing import Literal, NamedTuple
from unittest.mock import patch

from std_utils.more_str.generators import random_string, uuid_to_base64


class _UUIDToBase64Case(NamedTuple):
    """A test case for the uuid_to_base64 function."""

    uuid_type: Literal["uuid1", "uuid3", "uuid4", "uuid5"]
    frozen_uuid: str
    expected: str
    namespace: str = "not_required"


class StringGeneratorTestCase(unittest.TestCase):
    """Test cases for the string generator functions."""

    def test_uuid_to_base64(self) -> None:
        """Test the uuid_to_base64 function."""
        cases = (
            _UUIDToBase64Case(
                "uuid1",
                "ed908698-b908-11ef-9ee7-325096b39f47",
                "ZWQ5MDg2OThiOTA4MTFlZjllZTczMjUwOTZiMzlmNDc=",
            ),
            _UUIDToBase64Case(
                "uuid3",
                "ec1d345f-bb38-33c4-a7e1-ab6428265472",
                "ZWMxZDM0NWZiYjM4MzNjNGE3ZTFhYjY0MjgyNjU0NzI=",
                "test_namespace",
            ),
            _UUIDToBase64Case(
                "uuid4",
                "62e3e9bb-8f0a-49f1-b251-d073878f17ef",
                "NjJlM2U5YmI4ZjBhNDlmMWIyNTFkMDczODc4ZjE3ZWY=",
            ),
            _UUIDToBase64Case(
                "uuid5",
                "2857b1bd-ae52-5551-8287-eb6ef68cc6db",
                "Mjg1N2IxYmRhZTUyNTU1MTgyODdlYjZlZjY4Y2M2ZGI=",
                "test_namespace",
            ),
        )
        for case in cases:
            with (
                self.subTest(case=case, msg=f"{_UUIDToBase64Case}"),
                patch(f"uuid.{case.uuid_type}", return_value=uuid.UUID(case.frozen_uuid)),
            ):
                result = uuid_to_base64(case.uuid_type, case.namespace)
                self.assertEqual(result, case.expected)

    def test_random_string(self) -> None:
        """Test the random string generating function."""
        with patch("uuid.uuid4", return_value=uuid.UUID("62e3e9bb-8f0a-49f1-b251-d073878f17ef")):
            result = random_string()
            self.assertEqual(result, "NjJlM2U5YmI4ZjBhNDlmMWIyNTFkMDczODc4ZjE3ZWY=")
            self.assertRaises(ValueError, random_string, max_length=10)
            self.assertEqual(random_string(prefix="prefix_"), "prefix_NjJlM2U5YmI4ZjBhNDlmMWIyNTFkMDczODc4ZjE3ZWY=")
            self.assertEqual(random_string(suffix="_suffix"), "NjJlM2U5YmI4ZjBhNDlmMWIyNTFkMDczODc4ZjE3ZWY=_suffix")
            self.assertEqual(
                random_string(
                    prefix="prefix_",
                    suffix="_suffix",
                    randomizer=lambda: "test",
                ),
                "prefix_test_suffix",
            )
