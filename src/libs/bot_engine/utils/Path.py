from os.path import join, dirname, normpath, abspath
from os import getcwd

class Path:
    @staticmethod
    def relative_path(path: str) -> str:
        """ returns relative path for given folder """
        return normpath(join(getcwd(), path))