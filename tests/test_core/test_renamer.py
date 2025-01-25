import pytest
from core.renamer import Renamer

@pytest.fixture
def pattern() -> str:
    """
    Returns a pattern matching "test_name_###.EXT"
    with ### being exactly 3 digits and EXT being an extension.
    Example strings matching that pattern:
        test_name_001.txt
        test_name_123.zip
    """
    return "^test_name_\d{2}.?\S*$"


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
    found_files: list[str] = renamer.get_files_matching_pattern(files_to_check, pattern)
    assert len(found_files) == 2 and "test_name_001.txt" in found_files and "test_name_123.zip" in found_files


def test_get_files_matching_range_default_file_number_getting() -> None:
    file_list: list[str] = [
        "test_name_001.txt",    # Only this
        "test_name_123.zip",    # and this should be found to match the pattern
        "test_456.jpg"
    ]
    renamer = Renamer()
    files_matching_range: list[str] = renamer.get_files_matching_range(file_list, 123)
    assert len(files_matching_range) == 2 and "test_name_001.txt" in files_matching_range and "test_name_123.zip" in files_matching_range
