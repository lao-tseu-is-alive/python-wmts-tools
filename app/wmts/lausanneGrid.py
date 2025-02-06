import sys
from typing import Any, ClassVar
from pydantic import BaseModel
from app.wmts.utils import BBox


class LausanneGrid(BaseModel):
    """
    LausanneGrid class to handle the WMTS Swiss Grid system with 28 level of zoom (from 0 to 27).
        swissgrid_05:
        # https://www.ech.ch/dokument/473ea824-bbcd-43fa-ad0a-c7c84edfa1b8
        #resolutions: [4000, 2000, 1000, 500, 250, 100, 50, 20, 10, 5, 2.5, 1, 0.5, 0.25, 0.1, 0.05] valeurs Y. Jacolin
        resolutions: [50,20,10,5,2.5,1,0.5,0.25,0.1,0.05]
        # bbox [required]
        bbox: [2420000, 1030000, 2900000, 1350000] #valeurs c2c -NE PAS CHANGER, modifier la bbox dans la définition du layer-
        # srs [required]
        srs: EPSG:2056
    """
    MINX: ClassVar[float] = 2420000.0  # Minimum X coordinate in LV95 (EPSG:2056)
    MAXX: ClassVar[float] = 2900000.0
    MINY: ClassVar[float] = 1030000.0
    MAXY: ClassVar[float] = 1350000.0
    SpatialREF: ClassVar[int] = 2056  # SwissGrid LV95 (EPSG:2056)
    TileUrlTemplate: ClassVar[str] = '{zoom}/{tileRow}/{tileCol}.png'
    UNIT: ClassVar[str] = 'meters'
    MetersPerUnit: ClassVar[int] = 1
    TileSize: ClassVar[int] = 256
    top_left_x: ClassVar[float] = MINX  # top-left corner X in LV95 (EPSG:2056)
    top_left_y: ClassVar[float] = MAXY  # top-left corner Y in LV95 (EPSG:2056)
    tile_size: ClassVar[float] = TileSize  # Tile size in pixels

    # Resolution per zoom level in meters per pixel for SwissGrid_05
    resolutions: ClassVar[dict] = {
        0: {'ScaleDenominator': 178571.42857142858, 'cellSize': 50.0, 'MatrixWidth': 38.0, 'MatrixHeight': 25.0},
        1: {'ScaleDenominator': 71428.57142857143, 'cellSize': 20.0, 'MatrixWidth': 94.0, 'MatrixHeight': 63.0},
        2: {'ScaleDenominator': 35714.28571428572, 'cellSize': 10.0, 'MatrixWidth': 188.0, 'MatrixHeight': 125.0},
        3: {'ScaleDenominator': 17857.14285714286, 'cellSize': 5.0, 'MatrixWidth': 375.0, 'MatrixHeight': 250.0},
        4: {'ScaleDenominator': 8928.57142857143, 'cellSize': 2.5, 'MatrixWidth': 750.0, 'MatrixHeight': 500.0},
        5: {'ScaleDenominator': 3571.4285714285716, 'cellSize': 1.0, 'MatrixWidth': 1875.0, 'MatrixHeight': 1250.0},
        6: {'ScaleDenominator': 1785.7142857142858, 'cellSize': 0.5, 'MatrixWidth': 3750.0, 'MatrixHeight': 2500.0},
        7: {'ScaleDenominator': 892.8571428571429, 'cellSize': 0.25, 'MatrixWidth': 7500.0, 'MatrixHeight': 5000.0},
        8: {'ScaleDenominator': 357.14285714285717, 'cellSize': 0.1, 'MatrixWidth': 18750.0,'MatrixHeight': 12500.0}}

    def __init__(self, /, **data: Any):
        super().__init__(**data)

    def get_tile(self, coord_x: float, coord_y: float, zoom_level: int):
        # Check if zoom level is supported
        if zoom_level not in self.resolutions:
            raise ValueError("Unsupported zoom level. Please choose between 1 and 4.")

        # Get the resolution for the zoom level
        zoom_info = self.resolutions[zoom_level]
        resolution = zoom_info['cellSize']
        print(f"resolution: {resolution}")
        #resolution = self.resolutions[zoom_level]

        # Calculate the tile indices (x, y)
        tile_col = int((coord_x - self.top_left_x) / (self.tile_size * resolution))
        tile_row = int((self.top_left_y - coord_y) / (self.tile_size * resolution))

        return tile_col, tile_row

    def max_zoom(self):
        return max(self.resolutions.keys())

    def is_valid_tile(self, zoom_level: int, tile_col: int, tile_row: int):
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

    def get_tile_bbox(self, zoom_level: int, tile_col: int, tile_row: int) -> BBox | None:
        # Check if tile request is valid
        if self.is_valid_tile(zoom_level, tile_col, tile_row):
            zoom_info = self.resolutions[zoom_level]
            resolution = zoom_info['cellSize']
            x_min = self.top_left_x + tile_col * self.tile_size * resolution
            y_max = self.top_left_y - tile_row * self.tile_size * resolution
            x_max = x_min + self.tile_size * resolution
            y_min = y_max - self.tile_size * resolution
            return BBox(bbox=[x_min, y_min, x_max, y_max])
        else:
            # try to find why the tile indices are not valid
            if zoom_level not in self.resolutions:
                raise ValueError(f"Unsupported zoom level. Please choose between 0 and {self.max_zoom()}.")
            if tile_col < 0 or tile_col > self.get_max_num_cols(zoom_level):
                raise ValueError(
                    f"Invalid column index. Please choose between 0 and {self.get_max_num_cols(zoom_level)}.")
            if tile_row < 0 or tile_row > self.get_max_num_rows(zoom_level):
                raise ValueError(f"Invalid row index. Please choose between 0 and {self.get_max_num_rows(zoom_level)}.")
            return None

    def get_bbox(self):
        """
        Get the bounding box of the SwissGrid_05 in LV95 coordinates.
        return: Tuple of (x_min, y_min, x_max, y_max)
        """
        return [self.MINX, self.MINY, self.MAXX, self.MAXY]

    def get_tile_width(self):
        """
        Get the width of the tile in meters.
        return: Width of the tile in meters.
        """
        return self.tile_size * self.MetersPerUnit

    def get_tile_height(self):
        """
        Get the height of the tile in meters.
        return: Height of the tile in meters.
        """
        return self.tile_size * self.MetersPerUnit

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

    def get_max_num_rows(self, zoom_level: int):
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

    def get_max_num_cols(self, zoom_level: int):
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


def abort(status_code: int, message: str):
    sys.exit(f"{status_code}: {message}")


if __name__ == "__main__":
    # Example usage
    coordinate_x = 2538817  # X coordinate (SwissGrid LV95)
    coordinate_y = 1163422  # Y coordinate (SwissGrid LV95)
    col = 1838  # Row index
    row = 3083  # Column index
    zoom = 7  # Zoom level (1, 2, 3, or 4)
    srid = 2056  # SwissGrid LV95 (EPSG:2056)
    tilesMn95Template=f"https://tilesmn95.lausanne.ch/tiles/1.0.0/fonds_geo_osm_bdcad_couleur/default/2021/swissgrid_05/{zoom}/{row}/{col}.png"
    fonds_geo_osm_bdcad_couleur_layers = "osm_bdcad_couleur_msgroup,planville_cs_autres_msgroup,planville_cs_bati_pol_sout,planville_marquage_msgroup,planville_od_objets_msgroup,planville_arbres_goeland_msgroup,planville_cs_bati_msgroup,planville_od_labels_msgroup"

    print(f"bbox for a tile at zoom: {zoom}, col: {col}, row: {row} ")
    ch_grid = LausanneGrid()
    bbox = ch_grid.get_tile_bbox(zoom, col, row)
    print(f"swiss bbox: {repr(bbox)}")
    bbox_str = ','.join([str(b) for b in bbox.bbox])
    print (f"bbox string: {bbox}")
    wms_request=(f"https://carto.lausanne.ch/mapserv_proxy?ogcserver=source+for+image%2Fpng&SERVICE=WMS&" +
                 f"VERSION=1.3.0&REQUEST=GetMap&FORMAT=image%2Fpng&TRANSPARENT=true&" +
                 f"LAYERS={fonds_geo_osm_bdcad_couleur_layers}&SERVERTYPE=mapserver&STYLES=&CRS=EPSG%3A2056&" +
                 f"WIDTH=256&HEIGHT=256&" +
                 f"BBOX=" + bbox_str)
    print(f"wms_request:\n {wms_request}")
    print(tilesMn95Template)


    print("let's try an invalid request with a zoom of 129")
    try:
        bbox = ch_grid.get_tile_bbox(129, col, row)
    except ValueError as error:
        print(f"Error: {error}")
