from config import BuildConfig
import build123d as b3d
from yacv_server import show


def mkLid(config: BuildConfig):
    thickness = config.wallThickness
    cube = b3d.Box(
        length=config.lidPanelWidth * 2, width=config.width, height=thickness
    )
    cutPlane: b3d.Plane = (
        b3d.Plane.ZY * b3d.Rot((-config.lidLockAngle, 0, 0)) * b3d.Rot((0, 45, 0))
    )
    return cube.split(plane=cutPlane, keep=b3d.Keep.BOTTOM)


lid = mkLid(BuildConfig())
show(lid)
