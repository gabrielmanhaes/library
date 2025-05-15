from archiver.config import Config


class Blocker:
    def __init__(self):
        self.blocklist = Config.BLOCKLIST
        self.headers = [
            "authorization",
            "cookie",
            "accept",
            "accept-encoding",
            "accept-language",
            "cache-control",
            "connection",
            "pragma",
            "proxy-connection",
            "upgrade-insecure-requests",
        ]
        self.trailers = []

    def is_junk(self, domain: str) -> bool:
        return domain in self.blocklist

    def should_drop_header(self, header: str) -> bool:
        return header.lower() in self.headers

    def should_drop_trailer(self, trailer: str) -> bool:
        return trailer.lower() in self.trailers
