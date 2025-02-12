import logging
from app.wmts.lausanneGrid import LausanneGrid


# BBox of the image
imgXMin = 2539000.0
imgXMax = 2540000.0
imgYMin = 1154000.0
imgYMax = 1155000.0

# Basic Configuration (Simplest)
logging.basicConfig(level=logging.DEBUG)  # Set root logger to DEBUG

# More Control (Recommended)
logger = logging.getLogger(__name__)  # Get a logger for the current module
logger.setLevel(logging.WARNING)         # Set the logger's level


#trouver la grille de tuiles correspondant à la bbox
grid = LausanneGrid()

tileGridMaxX=imgXMax
tileGridMaxY=imgYMax
tileGridMinX=imgXMin
tileGridMinY=imgYMin

my_tileGridBboxByZoom = {}

for currentZoom in range(0, grid.max_zoom()):
    logger.debug(f"## currentZoom={currentZoom}")
    col,row = grid.get_tile(imgXMin, imgYMax, currentZoom)
    logger.debug(f"col={col}, row={row}")
    myBBox = grid.get_tile_bbox(currentZoom, col, row)
    bbox = myBBox.bbox
    #get the minX and maxY of the tile
    if bbox[0] < tileGridMinX:
        tileGridMinX = bbox[0]
    if bbox[3] > tileGridMaxY:
        tileGridMaxY = bbox[3]
    logger.info(f"## bboxTopLeft={bbox}")
    col,row = grid.get_tile(imgXMax, imgYMin, currentZoom)
    logger.debug(f"col={col}, row={row}")
    myBBox = grid.get_tile_bbox(currentZoom, col, row)
    bbox = myBBox.bbox
    #get the maxX and minY of the tile
    if bbox[2] > tileGridMaxX:
        tileGridMaxX = bbox[2]
    if bbox[1] < tileGridMinY:
        tileGridMinY = bbox[1]
    logger.info(f"## bboxBottomRight={bbox}")
    my_tileGridBboxByZoom[currentZoom] = [tileGridMinX, tileGridMinY, tileGridMaxX, tileGridMaxY]

logger.info(f"## imgBBox={imgXMin},{imgYMin},{imgXMax},{imgYMax}")
logger.info(f"## tileGridBBox={tileGridMinX},{tileGridMinY},{tileGridMaxX},{tileGridMaxY}")
print(f"## imgBBox={imgXMin},{imgYMin},{imgXMax},{imgYMax}")
for z in range(0, grid.max_zoom()):
    print(f"## zoom={z}, bbox={my_tileGridBboxByZoom[z]}")


