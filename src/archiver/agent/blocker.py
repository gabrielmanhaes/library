import fnmatch
from archiver.config import Config


class Blocker:
    def __init__(self):
        self.blocklist = Config.BLOCKLIST
        self.headers = [
            "User-Agent",
            "Cookie",
            "Accept",
            "Accept-Encoding",
            "Accept-Language",
            "Cache-Control",
            "Connection",
            "Pragma",
            "Proxy-Connection",
            "Upgrade-Insecure-Requests",
        ]

    def is_blocked(self, domain: str) -> bool:
        domain = domain.lower()
        return any(fnmatch.fnmatch(domain, entry) for entry in self.blocklist)

    def should_drop_trace(self, domain: str) -> bool:
        return self.is_blocked(domain)

    def should_drop_header(self, header: str) -> bool:
        return header in self.headers
