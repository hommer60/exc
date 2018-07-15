from unittest import TestCase
from unittest.mock import MagicMock, patch
import io
from gift_exchange.commands import import_file, register, reset
from types import SimpleNamespace

class TestCommands(TestCase):

    @patch("gift_exchange.commands.delete_directory")
    @patch("gift_exchange.commands.load_directory")
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_reset_empty_directory(self, mock_print, mock_load_directory, mock_delete_directory):
        mock_load_directory.return_value = {}
        reset(None)
        self.assertFalse(mock_delete_directory.called)

    @patch("gift_exchange.commands.delete_directory")
    @patch("gift_exchange.commands.load_directory")
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_reset_populated_directory(self, mock_print, mock_load_directory, mock_delete_directory):
        mock_load_directory.return_value = {"John" : None}
        reset(None)
        self.assertTrue(mock_delete_directory.called)

    @patch("gift_exchange.commands.save_directory")
    @patch("gift_exchange.commands.load_directory")
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_register_name_already_registered(self, mock_print, mock_load_directory, mock_save_directory):
        args = SimpleNamespace()
        args.name = ["John"]
        args.partner = None
        mock_load_directory.return_value = {"John" : None}
        register(args)
        self.assertFalse(mock_save_directory.called)

    @patch("gift_exchange.commands.save_directory")
    @patch("gift_exchange.commands.load_directory")
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_register_partner_already_registered(self, mock_print, mock_load_directory, mock_save_directory):
        args = SimpleNamespace()
        args.name = ["John"]
        args.partner = ["Mike"]
        mock_load_directory.return_value = {"Mike" : None}
        register(args)
        self.assertFalse(mock_save_directory.called)

    @patch("gift_exchange.commands.save_directory")
    @patch("gift_exchange.commands.load_directory")
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_register_partner_name_not_registered(self, mock_print, mock_load_directory, mock_save_directory):
        args = SimpleNamespace()
        args.name = ["John"]
        args.partner = ["Mike"]
        mock_load_directory.return_value = {}
        register(args)
        mock_save_directory.assert_called_once_with({"John" : "Mike", "Mike" : "John"})

    @patch("gift_exchange.commands.save_directory")
    @patch("gift_exchange.commands.load_directory")
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("sys.stderr", new_callable=io.StringIO)
    def test_register_name_not_registered(self, mock_stderr, mock_print, mock_load_directory, mock_save_directory):
        args = SimpleNamespace()
        args.name = ["John"]
        args.partner = None
        mock_load_directory.return_value = {}
        register(args)
        mock_save_directory.assert_called_once_with({"John" : None})

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("sys.stderr", new_callable=io.StringIO)
    def test_import_file_invalid_extension(self, mock_stderr, mock_print):
        filename = "file.fake"
        args = SimpleNamespace()
        args.filename = filename
        import_file(args)
        self.assertEquals(mock_print.getvalue(),
        "Must provide a .txt file, take a look at example_guest_list.txt for an example\n")

    @patch("builtins.open")
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_import_file_not_found(self, mock_print, mock_open):
        filename = "fake.txt"
        args = SimpleNamespace()
        args.filename = filename
        mock_open.side_effect = IOError()
        import_file(args)
        self.assertEquals(mock_print.getvalue(), "The specified file does not exist!\n")