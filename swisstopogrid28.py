import logging as logger
import sys

from wmts_grids import get_tile_grid

# Constants
# based on the OGC standard, which is based on the assumption of a screen resolution of 90.7 DPI (dots per inch).
WMTS_REF_PIXEL_SIZE_M = 0.00028 # Reference pixel size in meters


def get_scale_denominator(cell_size):
    """
    Get the scale denominator for a given cell_size (by zoom).
    scaleDenominator is used to define the scale at which a map tile is rendered.
     It specifies the relationship between a unit of distance on the map and the corresponding unit of distance on the ground.
    return: Scale denominator for the specified cell size.
    """
    return cell_size / WMTS_REF_PIXEL_SIZE_M


class SwissTopoGrid28:
    """
    SwissTopoGrid28 class to handle the WMTS Swiss Grid system with 28 level of zoom (from 0 to 27).
    like the TileMatrixSet 2056_28 from the SwissTopo WMTS service.
    more info:
    https://wmts.geo.admin.ch/EPSG/2056/1.0.0/WMTSCapabilities.xml?lang=fr
    https://www.ech.ch/de/ech/ech-0056/4.0.1
    https://www.ech.ch/sites/default/files/imce/eCH-Dossier/0031-0060/eCH-0056/4.0.1/Beilagen/eCH-0056-LV95CellSizes-4-0.json

    """
    MINX = 2420000.0 # Minimum X coordinate in LV95 (EPSG:2056)
    MAXX = 2900000.0
    MINY = 1030000.0
    MAXY = 1350000.0
    SpatialREF = 2056  # SwissGrid LV95 (EPSG:2056)
    TileUrlTemplate = '{zoom}/{tileCol}/{tileRow}'
    UNIT = 'meters'
    MetersPerUnit = 1
    TileSize = 256

    def __init__(self):
        self.top_left_x = self.MINX   # top-left corner X in LV95 (EPSG:2056)
        self.top_left_y = self.MAXY   # top-left corner Y in LV95 (EPSG:2056)
        self.tile_size = self.TileSize       # Tile size in pixels

        # Resolution per zoom level in meters per pixel for SwissGrid_05
        self.resolutions = {0: {'ScaleDenominator': 14285714.285714287, 'cellSize': 4000.0, 'MatrixWidth': 1.0, 'MatrixHeight': 1.0}, 1: {'ScaleDenominator': 13392857.142857144, 'cellSize': 3750.0, 'MatrixWidth': 1.0, 'MatrixHeight': 1.0}, 2: {'ScaleDenominator': 12500000.000000002, 'cellSize': 3500.0, 'MatrixWidth': 1.0, 'MatrixHeight': 1.0}, 3: {'ScaleDenominator': 11607142.857142858, 'cellSize': 3250.0, 'MatrixWidth': 1.0, 'MatrixHeight': 1.0}, 4: {'ScaleDenominator': 10714285.714285715, 'cellSize': 3000.0, 'MatrixWidth': 1.0, 'MatrixHeight': 1.0}, 5: {'ScaleDenominator': 9821428.571428573, 'cellSize': 2750.0, 'MatrixWidth': 1.0, 'MatrixHeight': 1.0}, 6: {'ScaleDenominator': 8928571.42857143, 'cellSize': 2500.0, 'MatrixWidth': 1.0, 'MatrixHeight': 1.0}, 7: {'ScaleDenominator': 8035714.285714286, 'cellSize': 2250.0, 'MatrixWidth': 1.0, 'MatrixHeight': 1.0}, 8: {'ScaleDenominator': 7142857.142857144, 'cellSize': 2000.0, 'MatrixWidth': 1.0, 'MatrixHeight': 1.0}, 9: {'ScaleDenominator': 6250000.000000001, 'cellSize': 1750.0, 'MatrixWidth': 2.0, 'MatrixHeight': 1.0}, 10: {'ScaleDenominator': 5357142.857142857, 'cellSize': 1500.0, 'MatrixWidth': 2.0, 'MatrixHeight': 1.0}, 11: {'ScaleDenominator': 4464285.714285715, 'cellSize': 1250.0, 'MatrixWidth': 2.0, 'MatrixHeight': 1.0}, 12: {'ScaleDenominator': 3571428.571428572, 'cellSize': 1000.0, 'MatrixWidth': 2.0, 'MatrixHeight': 2.0}, 13: {'ScaleDenominator': 2678571.4285714286, 'cellSize': 750.0, 'MatrixWidth': 3.0, 'MatrixHeight': 2.0}, 14: {'ScaleDenominator': 2321428.571428572, 'cellSize': 650.0, 'MatrixWidth': 3.0, 'MatrixHeight': 2.0}, 15: {'ScaleDenominator': 1785714.285714286, 'cellSize': 500.0, 'MatrixWidth': 4.0, 'MatrixHeight': 3.0}, 16: {'ScaleDenominator': 892857.142857143, 'cellSize': 250.0, 'MatrixWidth': 8.0, 'MatrixHeight': 5.0}, 17: {'ScaleDenominator': 357142.85714285716, 'cellSize': 100.0, 'MatrixWidth': 19.0, 'MatrixHeight': 13.0}, 18: {'ScaleDenominator': 178571.42857142858, 'cellSize': 50.0, 'MatrixWidth': 38.0, 'MatrixHeight': 25.0}, 19: {'ScaleDenominator': 71428.57142857143, 'cellSize': 20.0, 'MatrixWidth': 94.0, 'MatrixHeight': 63.0}, 20: {'ScaleDenominator': 35714.28571428572, 'cellSize': 10.0, 'MatrixWidth': 188.0, 'MatrixHeight': 125.0}, 21: {'ScaleDenominator': 17857.14285714286, 'cellSize': 5.0, 'MatrixWidth': 375.0, 'MatrixHeight': 250.0}, 22: {'ScaleDenominator': 8928.57142857143, 'cellSize': 2.5, 'MatrixWidth': 750.0, 'MatrixHeight': 500.0}, 23: {'ScaleDenominator': 7142.857142857143, 'cellSize': 2.0, 'MatrixWidth': 938.0, 'MatrixHeight': 625.0}, 24: {'ScaleDenominator': 5357.142857142858, 'cellSize': 1.5, 'MatrixWidth': 1250.0, 'MatrixHeight': 834.0}, 25: {'ScaleDenominator': 3571.4285714285716, 'cellSize': 1.0, 'MatrixWidth': 1875.0, 'MatrixHeight': 1250.0}, 26: {'ScaleDenominator': 1785.7142857142858, 'cellSize': 0.5, 'MatrixWidth': 3750.0, 'MatrixHeight': 2500.0}, 27: {'ScaleDenominator': 892.8571428571429, 'cellSize': 0.25, 'MatrixWidth': 7500.0, 'MatrixHeight': 5000.0}, 28: {'ScaleDenominator': 357.14285714285717, 'cellSize': 0.09999999999999999, 'MatrixWidth': 18750.0, 'MatrixHeight': 12500.0}}

    def get_tile(self, coord_x, coord_y, zoom_level):
        # Check if zoom level is supported
        if zoom_level not in self.resolutions:
            raise ValueError("Unsupported zoom level. Please choose between 1 and 4.")

        resolution = self.resolutions[zoom_level]

        # Calculate the tile indices (x, y)
        tile_x = int((coord_x - self.top_left_x) / (self.tile_size * resolution))
        tile_y = int((self.top_left_y - coord_y) / (self.tile_size * resolution))

        return tile_x, tile_y

    def max_zoom(self):
        return max(self.resolutions.keys())

    def is_valid_tile(self, zoom_level, tile_col, tile_row):
        """
        Check if the tile indices are valid.
        param: zoom_level: Zoom level of the tile.
        param: tile_col: Column index of the tile.
        param: tile_row: Row index of the tile.
        return: True if the tile indices are valid, False otherwise.
        """
        # Check if zoom level is supported
        if zoom_level not in self.resolutions:
            return False
        # Check if tile indices are valid
        if tile_col < 0 or tile_col > self.get_max_num_cols(zoom_level):
            return False
        if tile_row < 0 or tile_row > self.get_max_num_rows(zoom_level):
            return False
        return True

    def get_tile_bbox(self, zoom_level, tile_col, tile_row):
        # Check if tile request is valid
        if self.is_valid_tile(zoom_level, tile_col, tile_row):
            zoom_info = self.resolutions[zoom_level]
            resolution = zoom_info['cellSize']
            x_min = self.top_left_x + tile_col * self.tile_size * resolution
            y_max = self.top_left_y - tile_row * self.tile_size * resolution
            x_max = x_min + self.tile_size * resolution
            y_min = y_max - self.tile_size * resolution
            return [x_min, y_min, x_max, y_max]
        else:
            #try to find why the tile indices are not valid
            if zoom_level not in self.resolutions:
                raise ValueError(f"Unsupported zoom level. Please choose between 0 and {self.max_zoom()}.")
            if tile_col < 0 or tile_col > self.get_max_num_cols(zoom_level):
                raise ValueError(f"Invalid column index. Please choose between 0 and {self.get_max_num_cols(zoom_level)}.")
            if tile_row < 0 or tile_row > self.get_max_num_rows(zoom_level):
                raise ValueError(f"Invalid row index. Please choose between 0 and {self.get_max_num_rows(zoom_level)}.")
            return None


    def get_bbox(self):
        """
        Get the bounding box of the SwissGrid_05 in LV95 coordinates.
        return: Tuple of (x_min, y_min, x_max, y_max)
        """
        return [self.MINX, self.MINY, self.MAXX, self.MAXY]

    def get_height(self):
        """
        Get the total height of the Grid in meters.
        return: Height of the Swiss Grid in meters. usually 320000
        """
        x1, y1, x2, y2 = self.get_bbox()
        return y2 - y1

    def get_width(self):
        """
        Get the total width of the Grid_05 in meters.
        return: Width of the Swiss Grid in meters. usually 480000
        """
        x1, y1, x2, y2 = self.get_bbox()
        return x2 - x1

    def get_max_num_rows(self, zoom_level):
        """
        Get the maximum number of rows in the SwissGrid_05.
        param: zoom_level: Zoom level of the tile.
        return: Maximum number of rows in the SwissGrid_05.
        """
        # Check if zoom level is supported
        if zoom_level not in self.resolutions:
            raise ValueError("Unsupported zoom level. Please choose between 1 and 4.")
        zoom_info = self.resolutions[zoom_level]
        if 'MatrixHeight' in zoom_info:
            return zoom_info['MatrixHeight']
        if "cellSize" not in zoom_info:
            raise ValueError(f"cellSize was not found for zoom_level {zoom_level}.")
        cell_size = zoom_info['cellSize']
        return self.get_height() / (self.tile_size * cell_size)

    def get_max_num_cols(self, zoom_level):
        """
        Get the maximum number of columns in the SwissGrid_05.
        param: zoom_level: Zoom level of the tile.
        return: Maximum number of columns in the SwissGrid_05.
        """
        # Check if zoom level is supported
        if zoom_level not in self.resolutions:
            raise ValueError("Unsupported zoom level. Please choose between 1 and 4.")
        zoom_info = self.resolutions[zoom_level]
        if 'MatrixWidth' in zoom_info:
            return zoom_info['MatrixWidth']
        if "cellSize" not in zoom_info:
            raise ValueError(f"cellSize was not found for zoom_level {zoom_level}.")
        cell_size = zoom_info['cellSize']
        return self.get_width() / (self.tile_size * cell_size)



def abort(status_code, message):
    sys.exit(f"{status_code}: {message}")

if __name__ == "__main__":
    # Example usage
    coordinate_x = 2538817  # X coordinate (SwissGrid LV95)
    coordinate_y = 1163422  # Y coordinate (SwissGrid LV95)
    col = 4570              # Row index
    row = 7650                # Column index
    zoom = 28          # Zoom level (1, 2, 3, or 4)
    srid = 2056            # SwissGrid LV95 (EPSG:2056)
    grid = None
    try:
        grid = get_tile_grid(srid)()
    except AssertionError as error:
        logger.error('Unsupported srid %s: %s', srid, error)
        abort(400, f'Unsupported srid {srid}')
    if grid is None:
        logger.error('Unsupported srid %s', srid)
        abort(400, f'Unsupported srid {srid}')

    print(f"grid: {repr(grid)}")

    bbox= None
    try:
        bbox = grid.tileBounds(zoom, col, row)
    except AssertionError as error:
        logger.error(f'Unsupported zoom level {zoom} for srid {srid}: {error}')
        abort(400, f'Unsupported zoom level {zoom} for srid {srid}')
    print(f"bbox for a tile at zoom: {zoom}, col: {col}, row: {row} ")
    print(f"swiss bbox: {repr(bbox)}")
    ch_grid = SwissTopoGrid28()
    bbox = ch_grid.get_tile_bbox(zoom, col, row)
    print(f"swiss bbox: {repr(bbox)}")
