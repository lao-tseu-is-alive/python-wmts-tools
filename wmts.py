def calculate_wmts_tile(coordinate_x, coordinate_y, zoom):
    # SwissGrid_05 parameters (fixed)
    top_left_x = 420000   # top-left corner X in LV95 (EPSG:2056)
    top_left_y = 350000   # top-left corner Y in LV95 (EPSG:2056)
    tile_size = 256       # Tile size in pixels

    # Resolution per zoom level in meters per pixel for SwissGrid_05
    resolutions = {
        1: 4000,
        2: 2000,
        3: 1000,
        4: 500,
        # Add more zoom levels if needed
    }

    # Check if zoom level is supported
    if zoom not in resolutions:
        raise ValueError("Unsupported zoom level. Please choose between 1 and 4.")

    resolution = resolutions[zoom]

    # Calculate the tile indices (x, y)
    tile_x = int((coordinate_x - top_left_x) / (tile_size * resolution))
    tile_y = int((top_left_y - coordinate_y) / (tile_size * resolution))

    return tile_x, tile_y




if __name__ == "__main__":
    # Example usage
    coordinate_x = 2538817  # X coordinate (SwissGrid LV95)
    coordinate_y = 1163422  # Y coordinate (SwissGrid LV95)
    zoom_level = 3          # Zoom level (1, 2, 3, or 4)
    res_tile_x, res_tile_y = calculate_wmts_tile(coordinate_x, coordinate_y, zoom_level)
    print(f"Tile X: {res_tile_x}, Tile Y: {res_tile_y}")
