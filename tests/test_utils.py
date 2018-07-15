from unittest import TestCase
from unittest.mock import MagicMock, patch
from gift_exchange.utils import load_directory, save_directory, delete_directory, DIRECTORY_PATH

class TestDirectoryIO(TestCase):

    @patch("pickle.dump")
    @patch("builtins.open")
    def test_save_directory(self, mock_open, mock_pickle):
        file = mock_open.return_value
        file.method.return_value = DIRECTORY_PATH
        save_directory({})
        mock_open.assert_called_once_with(DIRECTORY_PATH, "wb")
        mock_pickle.assert_called_once_with({}, file)

    @patch("os.remove")
    def test_remove_directory(self, mock_remove):
        delete_directory()
        mock_remove.assert_called_once_with(DIRECTORY_PATH)
    
    @patch("pickle.load")
    @patch("builtins.open")
    def test_load_directory(self, mock_open, mock_pickle_load):
        file = mock_open.return_value
        file.method.return_value = DIRECTORY_PATH
        mock_pickle_load.return_value = {}
        result = load_directory()
        mock_open.assert_called_once_with(DIRECTORY_PATH, "rb")
        mock_pickle_load.assert_called_once_with(file)
        self.assertEqual({}, result)

    @patch("pickle.dump")
    @patch("pickle.load")
    @patch("builtins.open")
    def test_load_directory_exception(self, mock_open, mock_pickle_load, mock_pickle_dump):
        file = mock_open.return_value
        file.method.return_value = DIRECTORY_PATH
        mock_open.side_effect = [IOError(), file]
        directory = load_directory()
        self.assertEqual(directory, None)
