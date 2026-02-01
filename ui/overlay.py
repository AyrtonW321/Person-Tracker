import cv2 as cv


def draw_crosshair(frame_bgr, size=20, thickness=2):
    H, W = frame_bgr.shape[:2]
    cv.drawMarker(
        frame_bgr,
        (W // 2, H // 2),
        (255, 255, 255),
        markerType=cv.MARKER_CROSS,
        markerSize=size,
        thickness=thickness,
    )


def draw_tracking_overlay(frame_bgr, result):
    if not result.get("found", False):
        return

    bbox = result.get("bbox")
    center = result.get("center")
    if bbox is None or center is None:
        return

    x, y, w, h = bbox
    cx, cy = center

    cv.rectangle(frame_bgr, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv.circle(frame_bgr, (cx, cy), 6, (255, 0, 0), -1)
