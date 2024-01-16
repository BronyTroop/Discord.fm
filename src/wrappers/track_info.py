import pylast

from util import request_handler


class TrackInfo:
    name: str
    artist: str
    duration: int
    cover: str
    url: str

    def __init__(self, manager, lastfm_track: pylast.Track):
        self.name = lastfm_track.title
        self.artist = lastfm_track.artist.name
        self.cover = lastfm_track.get_cover_image(pylast.SIZE_LARGE)
        if self.cover is None:
            self.cover = 'https://raw.githubusercontent.com/EmanuelVH/Discord.fm/main/src/resources/lastfm.png'
        if self.cover == 'https://lastfm.freetls.fastly.net/i/u/174s/2a96cbd8b46e442fc41c2b86b821562f.png':
            self.cover = 'https://raw.githubusercontent.com/EmanuelVH/Discord.fm/main/src/resources/lastfm.png'
        self.url = lastfm_track.get_url()

        handler = request_handler.RequestHandler(
            manager, f'album for track "{self.name}"'
        )
        duration_request = handler.attempt_request(lastfm_track.get_duration)

        self.duration = duration_request

    def __eq__(self, other):
        if not isinstance(other, TrackInfo):
            # don't attempt to compare against unrelated types
            return NotImplemented

        is_equal = self.name == other.name and self.artist == other.artist
        return is_equal
