import pytest
from app.core.renamer import Renamer

@pytest.fixture
def pattern() -> str:
    """
    Returns a pattern matching "test_name_###.EXT"
    with ### being exactly 3 digits and EXT being an extension.
    Example strings matching that pattern:
        test_name_001.txt
        test_name_123.zip
    """
    return r"^test_name_\d{2}.?\S*$"


@pytest.mark.parametrize(
    "filename, number",
    [
        ("test_1", 1),
        ("test_12", 12),
        ("test_3.jpg", 3),
        ("test_34.png", 34),
        ("test_name_5", 5),
        ("test_name_56", 56),
        ("test_name_7.jpg", 7),
        ("test_name_78.exe", 78)
    ]
)
def test_get_file_number_from_name(filename: str, number: int) -> None:
    renamer = Renamer()
    assert renamer.get_file_number_from_name(filename) == number


def test_get_files_matching_pattern(pattern: str) -> None:
    files_to_check: list[str] = [
        "test_name_001.txt",    # Only this
        "test_name_123.zip",    # and this should be found to match the pattern
        "test_456.jpg",
        "test789.png"
    ]
    renamer = Renamer()
    found_files: list[str] = (
        renamer.get_files_matching_pattern(files_to_check, pattern)
    )
    assert (
        len(found_files) == 2
        and "test_name_001.txt" in found_files
        and "test_name_123.zip" in found_files
    )


def test_get_files_matching_range_default_file_number_getting() -> None:
    file_list: list[str] = [
        "test_name_001.txt",    # Only this
        "test_name_123.zip",    # and this should be found to match the pattern
        "test_456.jpg"
    ]
    renamer = Renamer()
    files_matching_range: list[str] = (
        renamer.get_files_matching_range(file_list, 123)
    )
    assert (
        len(files_matching_range) == 2
        and "test_name_001.txt" in files_matching_range
        and "test_name_123.zip" in files_matching_range
    )


def test_get_renaming_map_best_case() -> None:
    files_to_rename: list[str] = [
        "new_york.png",
        "test1.jpg",
        "tokyo25.mp4"
    ]
    expected: set[str] = {
        "holidays_1.png",
        "holidays_2.jpg",
        "holidays_3.mp4"
    }
    r = Renamer()
    new_names: set[str] = set(
        r.get_renaming_map(files_to_rename, "holidays", 1).values()
    )
    assert set(new_names) == expected


def test_get_renaming_map_some_files_already_renamed() -> None:
    """
    Only the files that need to be renamed
    should be returned in the renaming map
    """
    files_to_rename: list[str] = [
        # This file has a correct name,
        # but incorrect number (way outside the correct range!)
        "holidays_2077.v",
        "new_york.png",
        # This file already has a correct name and number in correct range
        "holidays_1.jpg",
        "tokyo25.mp4",
        # This file does too
        "holidays_3.pdf"
    ]
    expected: set[str] = {
        "holidays_2.v",
        "holidays_4.png",
        "holidays_5.mp4"
    }
    r = Renamer()
    new_names: set[str] = set(
        r.get_renaming_map(files_to_rename, "holidays", 1).values()
    )
    assert set(new_names) == expected


@pytest.mark.parametrize(
        "new_name, valid",
        [
            ("test", True),
            ("Test", True),
            ("test1", True),
            ("Test1", True),
            ("test-1", True),
            ("Test-1", True),
            ("test_1", True),
            ("Test_1", True),
            ("test 1", True),
            ("Test 1", True),
            ("test/1", False),
            ("test\1", False),
            ("test+1", False),
            ("test$1", False),
            ("test#1", False)
        ]
)
def test_new_name_validation_default_pattern(
    new_name: str,
    valid: bool
) -> None:
    """
    Checks the validation of new names using the default pattern
    """
    r = Renamer()
    assert r.validate_new_name(new_name) == valid
