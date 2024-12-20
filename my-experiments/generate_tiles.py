import os
import sys

from osgeo import gdal
import math

# Define the WMTS parameters
TILE_SIZE = 256
TILE_FORMAT = "image/png"
WMS_VERSION = "1.3.0"
SRS = "EPSG:2056"
LAYER_NAME = "swissgrid"  # Replace with your layer name

TOP_LEFT_X = 2420000
TOP_LEFT_Y = 1350000


# Define the GeoTIFF file path
GEOTIFF_PATH = "../orthophotos/2538000_1152000.tif"  # Replace with your GeoTIFF file path

# Function to generate a WMTS tile from the GeoTIFF
def generate_wmts_tile(geotiff_path, zoom, x, y):
    # Open the GeoTIFF dataset
    dataset = gdal.Open(geotiff_path, gdal.GA_ReadOnly)
    geotransform = dataset.GetGeoTransform()
    projection = dataset.GetProjection()

    # Calculate tile bounds in EPSG:2056
    tile_bbox = tile_to_bbox(zoom, x, y)

    # Reproject tile bounds to GeoTIFF projection
    source_srs = gdal.osr.SpatialReference()
    source_srs.ImportFromEPSG(2056)
    target_srs = gdal.osr.SpatialReference(wkt=projection)
    transform = gdal.osr.CoordinateTransformation(source_srs, target_srs)
    minX, minY, _ = transform.TransformPoint(tile_bbox[0], tile_bbox[1])
    maxX, maxY, _ = transform.TransformPoint(tile_bbox[2], tile_bbox[3])

    # Calculate pixel size and offset
    pixel_size_x = (maxX - minX) / TILE_SIZE
    pixel_size_y = (maxY - minY) / TILE_SIZE
    offset_x = (minX - geotransform[0]) / geotransform[1]
    offset_y = (minY - geotransform[3]) / geotransform[5]

    # Read raster data for the tile
    band = dataset.GetRasterBand(1)
    tile_data = band.ReadAsArray(
        int(offset_x), int(offset_y), TILE_SIZE, TILE_SIZE
    )

    # Create a new GeoTIFF dataset for the tile
    driver = gdal.GetDriverByName("GTiff")
    tile_dataset = driver.Create(
        f"tile_{zoom}_{x}_{y}.tif",
        TILE_SIZE,
        TILE_SIZE,
        1,
        gdal.GDT_Byte,
    )
    tile_dataset.SetGeoTransform(
        (
            tile_bbox[0],
            pixel_size_x,
            0,
            tile_bbox[3],
            0,
            -pixel_size_y,
        )
    )
    tile_dataset.SetProjection(source_srs.ExportToWkt())
    tile_band = tile_dataset.GetRasterBand(1)
    tile_band.WriteArray(tile_data)
    tile_band.FlushCache()

    # Translate the tile to PNG
    gdal.Translate(f"tile_{zoom}_{x}_{y}.png", tile_dataset, format="PNG")

    # Close the datasets
    tile_dataset = None
    dataset = None

# Function to calculate tile bounding box in EPSG:2056
def tile_to_bbox(zoom, x, y):
    # Define the origin and resolution for Swissgrid
    origin_x = TOP_LEFT_X
    origin_y = TOP_LEFT_Y
    resolution = 1000 / math.pow(2, zoom)

    minX = origin_x + x * TILE_SIZE * resolution
    maxY = origin_y - y * TILE_SIZE * resolution
    maxX = minX + TILE_SIZE * resolution
    minY = maxY - TILE_SIZE * resolution
    return [minX, minY, maxX, maxY]


# Example usage
if __name__ == "__main__":
    # open the GeoTIFF file passed as first argument if any
    if len(sys.argv) > 1:
        geotiff_path = sys.argv[1]
    else:
        # if no file is passed, use the default
        geotiff_path = GEOTIFF_PATH
    # verify file is readable
    if not os.access(geotiff_path, os.R_OK):
        print(f"File {geotiff_path} not readable")
        sys.exit(1)
    gdal.UseExceptions()
    # try to open the dataset
    try:
        dataset = gdal.Open(geotiff_path, gdal.GA_ReadOnly)
        # get the projection
        projection = dataset.GetProjection()
        print(f"Projection: {projection}")
        # get the geotransform
        geotransform = dataset.GetGeoTransform()
        print(f"GeoTransform: {geotransform}")
        # get the top left corner and pixel size and convert to number
        topLeftImgX = geotransform[0]
        topLeftImgY = geotransform[3]
        pixelSizeX = geotransform[1]
        pixelSizeY = geotransform[5]
        #check if the geotransform is valid and equal to swiss srid 2056
        if topLeftImgX < TOP_LEFT_X and topLeftImgY > TOP_LEFT_Y:
            print(f"Geotransform not valid, expected {topLeftImgX} >= {TOP_LEFT_X}, and {topLeftImgY} <= {TOP_LEFT_Y}")
            sys.exit(1)
        # get the width and height
        width = dataset.RasterXSize
        height = dataset.RasterYSize
        print(f"Width: {width} pixel, Height: {height}")
        #get the bounding box of the image
        minX = topLeftImgX
        maxY = topLeftImgY
        maxX = topLeftImgX + width * pixelSizeX
        minY = topLeftImgY + height * pixelSizeY
        print(f"Image bounding box minX,minY,maxX,maxY : {minX}, {minY}, {maxX}, {maxY}")
    except Exception as e:
        print(f"Error opening gdal dataset: {e}")
        sys.exit(1)


    # for now exit
    sys.exit(0)
    # Generate tiles for zoom levels 0 to 5 and a specific tile range
    #for zoom in range(0, 2):
    #    for x in range(0, 2**zoom):
    #        for y in range(0, 2**zoom):
    #            generate_wmts_tile(GEOTIFF_PATH, zoom, x, y)

    # Generate GetCapabilities XML
