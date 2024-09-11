

import pytest
from app.vision.fileclassifier import FileType

def test_file_type_enum_members():
    """
    Test that FileType enum contains exactly five members with correct values.
    """
    assert len(FileType) == 5
    assert FileType.MEDICAL_REPORT.value == "Medical_Report"
    assert FileType.WORK_ADMIN.value == "Work_Admin"
    assert FileType.WORK_PTO.value == "Work_PTO"
    assert FileType.CPA.value == "CPA"
    assert FileType.OTHER.value == "Other"

def test_file_type_enum_uniqueness():
    """
    Test that each FileType enum member is unique.
    """
    file_types = list(FileType)
    assert len(file_types) == len(set(file_types))

def test_file_type_enum_string_match():
    """
    Test that the string value of each FileType enum member matches its name in uppercase.
    """
    for file_type in FileType:
        assert file_type.name == file_type.value.upper()

def test_file_type_enum_immutability():
    """
    Test that FileType enum values are constant and cannot be changed.
    """
    with pytest.raises(AttributeError):
        FileType.MEDICAL_REPORT = "NewValue"

def test_file_type_creation_from_string():
    """
    Test creating FileType enum members from string values.
    """
    assert FileType("Work_Admin") == FileType.WORK_ADMIN
    assert FileType("Medical_Report") == FileType.MEDICAL_REPORT

def test_file_type_is_valid_type():
    """
    Test the is_valid_type class method of FileType.
    """
    assert FileType.is_valid_type("Medical_Report") == True
    assert FileType.is_valid_type("Work_Admin") == True
    assert FileType.is_valid_type("Work_PTO") == True
    assert FileType.is_valid_type("CPA") == True
    assert FileType.is_valid_type("Other") == True
    assert FileType.is_valid_type("InvalidType") == False

def test_file_type_is_valid_type_case_sensitivity():
    """
    Test that is_valid_type method is case-sensitive.
    """
    assert FileType.is_valid_type("medical_report") == False
    assert FileType.is_valid_type("MEDICAL_REPORT") == False

@pytest.mark.parametrize("invalid_input", [None, 123, True, []])
def test_file_type_is_valid_type_invalid_inputs(invalid_input):
    """
    Test is_valid_type method with invalid inputs.

    Preconditions:
    - FileType.is_valid_type method exists and expects a string input

    Postconditions:
    - TypeError is raised for non-string inputs

    Edge Cases:
    - None, integers, booleans, and other non-string types are tested
    """
    with pytest.raises(TypeError):
        FileType.is_valid_type(invalid_input)

def test_file_type_is_valid_type_empty_string():
    """
    Test is_valid_type method with an empty string.

    Preconditions:
    - FileType.is_valid_type method exists and expects a non-empty string input

    Postconditions:
    - Returns False for an empty string input

    Edge Cases:
    - Empty string is a valid string but not a valid FileType
    """
    assert FileType.is_valid_type("") == False

@pytest.mark.parametrize("valid_input", ["Medical_Report", "Work_Admin", "Work_PTO", "CPA", "Other"])
def test_file_type_is_valid_type_valid_inputs(valid_input):
    """
    Test is_valid_type method with valid inputs.

    Preconditions:
    - FileType.is_valid_type method exists
    - FileType enum contains the expected members

    Postconditions:
    - Returns True for all valid FileType values

    Invariants:
    - The set of valid FileTypes remains constant
    """
    assert FileType.is_valid_type(valid_input) == True

def test_file_type_is_valid_type_invalid_string():
    """
    Test is_valid_type method with an invalid string.

    Preconditions:
    - FileType.is_valid_type method exists

    Postconditions:
    - Returns False for a string that is not a valid FileType

    Edge Cases:
    - A non-empty string that doesn't match any FileType
    """
    assert FileType.is_valid_type("InvalidFileType") == False
