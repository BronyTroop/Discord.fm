from unittest import main, TestCase
from unittest.mock import MagicMock, patch, DEFAULT

import pylast

from wrappers import discord_rp, last_fm_user, track_info


class TestLastFm(TestCase):
    data = pylast.Track("TestArtist", "TestTitle", None, "TestUsername")
    error = pylast.WSError(None, None, "User not found")
    usernames = {"test": True, "TEST01": False, "andodide": True, "androidWG": False}

    def test_invalid_username(self):
        manager = MagicMock()
        manager.settings.get.return_value = ""

        with self.assertRaises(ValueError):
            last_fm_user.LastFMUser(manager)

    @patch("os.environ.get")
    @patch("util.request_handler.RequestHandler.attempt_request")
    def test_check_username(self, mock_request_handler: MagicMock, *mock):
        """Test if the check_username function is correctly handling exceptions from pylast"""
        mock_request_handler.side_effect = [
            self.data,
            self.error,
            self.data,
            self.error,
        ]

        for name in self.usernames.keys():
            manager = MagicMock()
            manager.settings.get.return_value(name)
            user = last_fm_user.LastFMUser(manager)

            result = user.check_username()
            print(result)
            self.assertEqual(result, self.usernames[name])

    @patch("util.request_handler.RequestHandler.attempt_request")
    @patch("wrappers.track_info.TrackInfo")
    def test_now_playing(
        self, mock_track_info: MagicMock, mock_request_handler: MagicMock
    ):
        """Test if now_playing properly handles None objects and"""
        mock = MagicMock(name="TestTitle", artist="TestArtist", duration=2852)
        mock_track_info.return_value = mock
        mock_request_handler.side_effect = [None, self.data, self.data]

        manager = MagicMock()
        manager.settings.get.return_value(list(self.usernames)[0])

        user = last_fm_user.LastFMUser(manager)

        result1 = user.now_playing()
        result2 = user.now_playing()
        result3 = user.now_playing()

        self.assertIsNone(result1)
        self.assertEqual(result2, mock)
        self.assertEqual(result3, mock)
        mock_track_info.assert_called_once()


class TestDiscordRP(TestCase):
    title = "TestTitle"
    artist = "TestArtist"
    artist2 = "TestArtist2"

    data1 = MagicMock(name=title, artist=artist2, duration=5005)
    data2 = MagicMock(name=title, artist=artist, duration=2852)

    @patch.object(discord_rp, "logger")
    @patch("pypresence.utils")
    def test_update_status(self, *mocks):
        """Test if status updates function correctly with TrackInfo objects"""
        rp = discord_rp.DiscordRP()

        rp.presence = MagicMock()

        rp.update_status(self.data1)
        rp.update_status(self.data2)
        rp.update_status(self.data2)

        with self.assertRaises(AttributeError):
            rp.update_status(None)

    @patch("asyncio.get_event_loop")
    def test_connect_disconnect(self, *mocks):
        rp = discord_rp.DiscordRP()
        rp.presence = MagicMock()

        rp.connect()
        rp.disconnect()

        rp.presence = None
        rp.connect()
        self.assertIsNotNone(rp.presence)


class TestTrackInfo(TestCase):
    title = "TestTitle"
    artist = "TestArtist"
    artist2 = "TestArtist2"
    duration = 2852

    data1 = pylast.Track(artist, title, None, "TestUsername")
    data2 = pylast.Track(artist2, title, None, "TestUsername")

    manager = MagicMock()

    @patch("pylast.Track.get_cover_image")
    @patch("util.request_handler.RequestHandler.attempt_request")
    def test_values(self, mock_request_handler: MagicMock, mock_cover: MagicMock):
        mock_request_handler.return_value = self.duration

        result = track_info.TrackInfo(self.manager, self.data1)

        self.assertEqual(result.name, self.title)
        self.assertEqual(result.artist, self.artist)
        self.assertEqual(result.duration, self.duration)

    @patch("pylast.Track.get_cover_image")
    @patch("util.request_handler.RequestHandler.attempt_request")
    def test_equal(self, mock_request_handler: MagicMock, mock_cover: MagicMock):
        mock_request_handler.return_value = self.duration

        info1 = track_info.TrackInfo(self.manager, self.data1)
        info2 = track_info.TrackInfo(self.manager, self.data1)
        info3 = track_info.TrackInfo(self.manager, self.data2)

        self.assertEqual(info1, info2, "Track info gathered is different!")
        self.assertNotEqual(info1, info3, "Track info gathered is not different!")


if __name__ == "__main__":
    main()
