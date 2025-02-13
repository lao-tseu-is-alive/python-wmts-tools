import logging
from app.wmts.lausanneGrid import LausanneGrid

# BBox of the image
imgXMin = 2537000.0
imgXMax = 2537999.975
imgYMin = 1152000.025
imgYMax = 1153000.0

# Basic Configuration (Simplest)
logging.basicConfig(level=logging.DEBUG)  # Set root logger to DEBUG

# More Control (Recommended)
logger = logging.getLogger(__name__)  # Get a logger for the current module
logger.setLevel(logging.WARNING)         # Set the logger's level


#trouver la grille de tuiles correspondant à la bbox
grid = LausanneGrid()


my_tileGridBboxByZoom = {}
for currentZoom in range(0, grid.num_zoom_levels()):
    logger.debug(f"## currentZoom={currentZoom}")
    col,row = grid.get_tile(imgXMin, imgYMax, currentZoom)
    logger.debug(f"col={col}, row={row}")
    myBBox = grid.get_tile_bbox(currentZoom, col, row)
    bbox = myBBox.bbox
    #get the minX and maxY of the tile
    tileGridMinX = bbox[0]
    tileGridMaxY = bbox[3]
    logger.info(f"## bboxTopLeft={bbox}")
    col,row = grid.get_tile(imgXMax, imgYMin, currentZoom)
    logger.debug(f"col={col}, row={row}")
    myBBox = grid.get_tile_bbox(currentZoom, col, row)
    bbox = myBBox.bbox
    #get the maxX and minY of the tile
    tileGridMaxX = bbox[2]
    tileGridMinY = bbox[1]
    logger.info(f"## bboxBottomRight={bbox}")
    my_tileGridBboxByZoom[currentZoom] = [tileGridMinX, tileGridMinY, tileGridMaxX, tileGridMaxY]

logger.info(f"## imgBBox={imgXMin},{imgYMin},{imgXMax},{imgYMax}")
print(f"## imgBBox={imgXMin},{imgYMin},{imgXMax},{imgYMax}")
for z in range(0, grid.num_zoom_levels()):
    print(f"## zoom={z}, bbox={my_tileGridBboxByZoom[z]}")


