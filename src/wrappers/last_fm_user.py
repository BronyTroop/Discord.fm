import logging
from typing import Callable, Tuple

import pylast

import util
from wrappers import track_info

logger = logging.getLogger("discord_fm").getChild(__name__)


class LastFMUser:
    _last_request: Tuple[pylast.Track, track_info.TrackInfo] = (None, None)

    def __init__(self, manager, inactive_func: Callable = None):
        self.m = manager
        username = self.m.settings.get("username")
        logger.debug(f'Reloading LastFMUser with username "{username}"')

        if username == "":
            raise ValueError("Username is empty")

        network = pylast.LastFMNetwork(api_key="b78db4c54979561c8cc742066a61fb39")

        self.username = username
        self.inactive_func = inactive_func
        self.user = network.get_user(username)

    def now_playing(self):
        handler = util.request_handler.RequestHandler(
            self.m, "user's Now Playing", self.inactive_func
        )
        request = handler.attempt_request(self.user.get_now_playing)

        if request == self._last_request[0]:
            return self._last_request[1]
        elif request is not None:
            info = track_info.TrackInfo(self.m, request)
            self._last_request = (request, info)
            return info
        else:
            return None

    def check_username(self):
        try:
            handler = util.request_handler.RequestHandler(self.m, "username validity")
            handler.attempt_request(self.user.get_now_playing)
            return True
        except pylast.WSError as e:
            if e.details == "User not found":
                return False
