import os


def get_path_to(path: str) -> str:
    return os.path.join(
        os.path.dirname(__file__),
        '../..',
        path,
    )
