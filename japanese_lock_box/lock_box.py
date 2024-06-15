from dataclasses import replace
from config import BuildConfig
import build123d as b3d
from project_paths import paths


def mkWholeBox(config: BuildConfig) -> b3d.Part:
    box = b3d.Part() + b3d.Box(config.length, config.width, config.height)
    return box.fillet(radius=config.filletRadius, edge_list=box.edges())


def mkInnerBox(config: BuildConfig) -> b3d.Part:
    w = config.wallThickness
    box = b3d.Box(config.length - 2 * w, config.width - 2 * w, config.height)
    return b3d.Location((0, 0, w)) * box


def slideLeftPlane(config: BuildConfig) -> b3d.Plane:
    cutPlane = b3d.Plane(
        (config.length / 2 - config.lidPanelLength * 2, 0, config.height / 2),
        (0, 0, 1),
        (-1, 0, 0),
    )
    return cutPlane.rotated(
        (-config.sildeHorizontalAngle, config.slideTaper, 0),
    )


def slideRightPlane(config: BuildConfig) -> b3d.Plane:
    return b3d.Plane.ZY.offset(-config.length / 2 + config.lidPanelLength)


def lidLeftPlane(config: BuildConfig) -> b3d.Plane:
    return b3d.Plane.ZY.offset(config.length / 2 - config.lidPanelLength)


def lidTopPlane(config: BuildConfig) -> b3d.Plane:
    return b3d.Plane.XY.offset(config.height / 2 - config.lidThicknessTop)


def mkSlide(config: BuildConfig) -> b3d.Part:
    slide = mkWholeBox(config)
    slide = slide.split(lidTopPlane(config))
    slide = slide.split(slideRightPlane(config))
    slide = slide.split(
        slideLeftPlane(config).offset(config.nozzle / 2), keep=b3d.Keep.BOTTOM
    )
    return slide


def mkBox(config: BuildConfig) -> b3d.Part:
    wholeBox = mkWholeBox(config)
    return mkBoxTopPanels(wholeBox, config) + mkBoxBottom(wholeBox, config)


def mkBoxTopPanels(box: b3d.Part, config: BuildConfig) -> b3d.Part:
    top = box.split(plane=lidTopPlane(config))
    return top - b3d.Box(
        config.length - 2 * config.lidPanelLength, config.width, config.height
    )


def mkBoxBottom(box: b3d.Part, config: BuildConfig) -> b3d.Part:
    topPlane = lidTopPlane(config)
    bottom = box.split(plane=topPlane, keep=b3d.Keep.BOTTOM)
    bottom -= mkInnerBox(config)
    return bottom - mkLidBoxConnectSub(config)


def mkLidBoxConnectSub(config: BuildConfig) -> b3d.Part:
    topPlane = lidTopPlane(config)
    subTopRect: b3d.Sketch = (
        topPlane
        * b3d.Location((0, 0, 0))
        * b3d.Rectangle(
            config.length - 2 * config.lidPanelLength + config.nozzle,
            config.width + config.nozzle,
        )
    )
    return b3d.extrude(subTopRect, amount=-config.wallThickness, taper=45)


def mkLidBottom(config: BuildConfig) -> b3d.Part:
    topPlane = lidTopPlane(config)
    w = config.wallThickness + config.nozzle / 2
    sketch: b3d.Sketch = (
        topPlane
        * b3d.Location((-config.lidBotomDelta, 0, 0))
        * b3d.Rectangle(
            config.length - 2 * config.lidPanelLength - 2 * w, config.width - 2 * w
        )
    )
    return mkLidBoxConnectSub(replace(config, nozzle=0)) + b3d.extrude(
        sketch, amount=-config.lidThicknessBelow
    )


def mkLidTop(box: b3d.Part, config: BuildConfig) -> b3d.Part:
    topPlane = lidTopPlane(config)
    topPart = box.split(topPlane)
    topPart = topPart.split(plane=lidLeftPlane(config), keep=b3d.Keep.BOTTOM).split(
        slideLeftPlane(replace(config, nozzle=0))
    )
    return topPart


def mkLid(config: BuildConfig) -> b3d.Part:
    box = mkWholeBox(config)
    return mkLidBottom(config) + mkLidTop(box, config)


box = mkBox(BuildConfig())
lid = mkLid(BuildConfig())
slide = mkSlide(BuildConfig())
b3d.export_stl(box, (paths.stls / "box.stl").as_posix())
b3d.export_stl(lid, (paths.stls / "lid.stl").as_posix())
b3d.export_stl(slide, (paths.stls / "slide.stl").as_posix())
