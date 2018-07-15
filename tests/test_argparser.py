import io
from unittest import TestCase
from unittest.mock import MagicMock, patch
from gift_exchange.argparser import parse_args

class TestParseArgs(TestCase):

    @patch("sys.stderr", new_callable=io.StringIO)
    def test_import_no_params(self, mock_stderr):
        with self.assertRaises(SystemExit) as cm:
            parse_args(["import"])
        exit_exception = cm.exception
        self.assertEqual(exit_exception.code, 2)
    
    @patch("sys.stderr", new_callable=io.StringIO)
    def test_import_too_many_params(self, mock_stderr):
        with self.assertRaises(SystemExit) as cm:
            parse_args(["import", "fakefile1.txt", "fakefile2.txt"])
        exit_exception = cm.exception
        self.assertEqual(exit_exception.code, 2)

    def test_import_valid_param(self):
        parsed_args = parse_args(["import", "fakefile.txt"])
        self.assertEqual(parsed_args.command, "import")
        self.assertEqual(parsed_args.filename, "fakefile.txt")

    @patch("sys.stderr", new_callable=io.StringIO)
    def test_register_no_name(self, mock_stderr):
        with self.assertRaises(SystemExit) as cm:
            parse_args(["register"])
        exit_exception = cm.exception
        self.assertEqual(exit_exception.code, 2)

    def test_register_one_name(self):
        parsed_args = parse_args(["register", "John"])
        self.assertEqual(parsed_args.command, "register")
        self.assertEqual(parsed_args.name, ["John"])

    def test_register_multiple_name(self):
        parsed_args = parse_args(["register", "John", "Boyer"])
        self.assertEqual(parsed_args.command, "register")
        self.assertEqual(parsed_args.name, ["John", "Boyer"])

    @patch("sys.stderr", new_callable=io.StringIO)
    def test_register_partner_no_name(self, mock_stderr):
        with self.assertRaises(SystemExit) as cm:
            parse_args(["register", "-p", "John"])
        exit_exception = cm.exception
        self.assertEqual(exit_exception.code, 2)

    @patch("sys.stderr", new_callable=io.StringIO)
    def test_register_partner_no_partner(self, mock_stderr):
        with self.assertRaises(SystemExit) as cm:
            parse_args(["register", "John", "-p"])
        exit_exception = cm.exception
        self.assertEqual(exit_exception.code, 2)

    def test_register_partner_one_partner_name(self):
        parsed_args = parse_args(["register", "John", "-p", "Mike"])
        self.assertEqual(parsed_args.command, "register")
        self.assertEqual(parsed_args.name, ["John"])
        self.assertEqual(parsed_args.partner, ["Mike"])

    def test_register_partner_multiple_partner_names(self):
        parsed_args = parse_args(["register", "John", "-p", "Mike", "Goodman"])
        self.assertEqual(parsed_args.command, "register")
        self.assertEqual(parsed_args.name, ["John"])
        self.assertEqual(parsed_args.partner, ["Mike", "Goodman"])

    def test_exchange_no_params(self):
        parsed_args = parse_args(["exchange"])
        self.assertEqual(parsed_args.command, "exchange")

    @patch("sys.stderr", new_callable=io.StringIO)
    def test_exchange_with_params(self, mock_stderr):
        with self.assertRaises(SystemExit) as cm:
            parse_args(["exchange", "fakeparam"])
        exit_exception = cm.exception
        self.assertEqual(exit_exception.code, 2)

    def test_reset_no_params(self):
        parsed_args = parse_args(["reset"])
        self.assertEqual(parsed_args.command, "reset")

    @patch("sys.stderr", new_callable=io.StringIO)
    def test_reset_with_params(self, mock_stderr):
        with self.assertRaises(SystemExit) as cm:
            parse_args(["reset", "fakeparam"])
        exit_exception = cm.exception
        self.assertEqual(exit_exception.code, 2)

    def test_guests_no_params(self):
        parsed_args = parse_args(["guests"])
        self.assertEqual(parsed_args.command, "guests")

    @patch("sys.stderr", new_callable=io.StringIO)
    def test_guests_with_params(self, mock_stderr):
        with self.assertRaises(SystemExit) as cm:
            parse_args(["guests", "fakeparam"])
        exit_exception = cm.exception
        self.assertEqual(exit_exception.code, 2)

    @patch("sys.stderr", new_callable=io.StringIO)
    def test_fake_command(self, mock_stderr):
        with self.assertRaises(SystemExit) as cm:
            parse_args(["fakecommand"])
        exit_exception = cm.exception
        self.assertEqual(exit_exception.code, 2)

    @patch("sys.stderr", new_callable=io.StringIO)
    def test_no_command(self, mock_stderr):
        with self.assertRaises(SystemExit) as cm:
            parse_args([])
        exit_exception = cm.exception
        self.assertEqual(exit_exception.code, 2)
        