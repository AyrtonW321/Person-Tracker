import config
from vision.colour_tracker import ColourTracker
from vision.person_tracker import PersonTracker
from vision.face_tracker import FaceTracker


def make_tracker(mode: str):
    mode = (mode or "").lower()

    if mode == "colour":
        return ColourTracker()

    if mode == "person":
        return PersonTracker()

    if mode == "face":
        return FaceTracker()

    raise ValueError(f"Unknown TRACK_MODE: {mode}")