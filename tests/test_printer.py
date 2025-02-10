import os
import pytest
from unittest.mock import MagicMock

from src.utils.printer import find_available_printers, print_document


class TestPrinter:

    # Returns a list of available printers when there are printers connected to the system
    def test_returns_list_of_available_printers(self):
        # Arrange

        # Act
        result = find_available_printers()

        # Assert
        assert isinstance(result, list)
        assert len(result) > 0

    # Returns an empty list when the 'wmic printer get name' command returns an error
    def test_returns_empty_list_on_error(self):
        # Arrange

        os.popen = MagicMock(side_effect=Exception("Error executing command"))

        # Act
        result = []
        try:
            result = find_available_printers()
        except Exception as e:
            # Assert
            assert isinstance(result, list)
            assert len(result) == 0
            assert str(e) == "Error executing command"

        # Prints a document using the default printer if no printer name is provided

    def test_unverified_printer_status(self, mocker):
        # Mock the necessary function
        mocker.patch("src.printer.verify_printer_status", return_value=False)

        # Call the function under test
        result = print_document("document.txt")

        # Assert that the result is None
        assert result is None

        # Uses the 'lp' command to print the document

    def test_uses_lp_command_to_print_document(self, mocker):
        # Mock the necessary functions
        mocker.patch("src.printer.verify_printer_status", return_value=True)
        mocker.patch(
            "src.printer.find_available_printers",
            return_value=["OneNote (Desktop)", "Microsoft Print to PDF"],
        )
        mocker.patch("os.system")

        # Call the function under test
        print_document("document.txt")

        # Assert that the correct command is executed
        os.system.assert_called_with("lp -d OneNote (Desktop) document.txt")
