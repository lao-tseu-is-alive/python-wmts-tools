# Constants
# based on the OGC standard, which is based on the assumption of a screen resolution of 90.7 DPI (dots per inch).
from pydantic import conlist, BaseModel

WMTS_REF_PIXEL_SIZE_M = 0.00028  # Reference pixel size in meters


class BBox(BaseModel):
    bbox: conlist(float, min_length=4, max_length=4)
    def __str__(self):
        return f"{self.bbox[0]},{self.bbox[1]},{self.bbox[2]},{self.bbox[3]}"


def get_scale_denominator(cell_size):
    """
    Get the scale denominator for a given cell_size (by zoom).
    scaleDenominator is used to define the scale at which a map tile is rendered.
     It specifies the relationship between a unit of distance on the map and the corresponding unit of distance on the ground.
    return: Scale denominator for the specified cell size.
    """
    return cell_size / WMTS_REF_PIXEL_SIZE_M


