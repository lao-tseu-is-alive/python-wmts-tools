import xml.etree.ElementTree as ET
WMTS_REF_PIXEL_SIZE_M = 0.00028 # Reference pixel size in meters
def xml_to_dict(xml_string):
    """
    Converts an TileMatrix XML string to a Python dictionary.

    Args:
        xml_string: The XML string to convert.

    Returns:
        A dictionary representing the XML data.
    """

    root = ET.fromstring(xml_string)
    result = {}

    # Handle the root's children
    for index,child in enumerate(root):
        tag = child.tag.split('}')[-1] # Remove namespace
        if tag == 'TileMatrix':
            tile_matrix_zoom = {}
            tile_matrix_data = {}
            for element in child:
                element_tag = element.tag.split('}')[-1] # Remove namespace

                # keep only the relevant elements
                if element_tag in ('ScaleDenominator', 'MatrixWidth', 'MatrixHeight'):
                    # Convert text to appropriate data type
                    if element_tag in ('ScaleDenominator', 'TileWidth', 'TileHeight', 'MatrixWidth', 'MatrixHeight'):
                        try:
                            tile_matrix_data[element_tag] = float(element.text) # Try float first
                        except ValueError:
                            tile_matrix_data[element_tag] = int(element.text)
                    elif element_tag == 'TopLeftCorner':
                        tile_matrix_data[element_tag] = [float(x) for x in element.text.split()]
                    else:
                        tile_matrix_data[element_tag] = element.text
                tile_matrix_data['cellSize'] = tile_matrix_data['ScaleDenominator'] * WMTS_REF_PIXEL_SIZE_M


            tile_matrix_zoom[index]=tile_matrix_data
            result.update(tile_matrix_zoom)

    return result


# Example usage with the above XML data:
xml_data = """
<TileMatrixSet>
<TileMatrix>
<ScaleDenominator>14285714.285714287</ScaleDenominator>
<TopLeftCorner>2420000.0 1350000.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>1</MatrixWidth>
<MatrixHeight>1</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ScaleDenominator>13392857.142857144</ScaleDenominator>
<TopLeftCorner>2420000.0 1350000.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>1</MatrixWidth>
<MatrixHeight>1</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ScaleDenominator>12500000.000000002</ScaleDenominator>
<TopLeftCorner>2420000.0 1350000.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>1</MatrixWidth>
<MatrixHeight>1</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ScaleDenominator>11607142.857142858</ScaleDenominator>
<TopLeftCorner>2420000.0 1350000.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>1</MatrixWidth>
<MatrixHeight>1</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ScaleDenominator>10714285.714285715</ScaleDenominator>
<TopLeftCorner>2420000.0 1350000.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>1</MatrixWidth>
<MatrixHeight>1</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ScaleDenominator>9821428.571428573</ScaleDenominator>
<TopLeftCorner>2420000.0 1350000.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>1</MatrixWidth>
<MatrixHeight>1</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ScaleDenominator>8928571.42857143</ScaleDenominator>
<TopLeftCorner>2420000.0 1350000.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>1</MatrixWidth>
<MatrixHeight>1</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ScaleDenominator>8035714.285714286</ScaleDenominator>
<TopLeftCorner>2420000.0 1350000.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>1</MatrixWidth>
<MatrixHeight>1</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ScaleDenominator>7142857.142857144</ScaleDenominator>
<TopLeftCorner>2420000.0 1350000.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>1</MatrixWidth>
<MatrixHeight>1</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ScaleDenominator>6250000.000000001</ScaleDenominator>
<TopLeftCorner>2420000.0 1350000.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>2</MatrixWidth>
<MatrixHeight>1</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ScaleDenominator>5357142.857142857</ScaleDenominator>
<TopLeftCorner>2420000.0 1350000.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>2</MatrixWidth>
<MatrixHeight>1</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ScaleDenominator>4464285.714285715</ScaleDenominator>
<TopLeftCorner>2420000.0 1350000.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>2</MatrixWidth>
<MatrixHeight>1</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ScaleDenominator>3571428.571428572</ScaleDenominator>
<TopLeftCorner>2420000.0 1350000.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>2</MatrixWidth>
<MatrixHeight>2</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ScaleDenominator>2678571.4285714286</ScaleDenominator>
<TopLeftCorner>2420000.0 1350000.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>3</MatrixWidth>
<MatrixHeight>2</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ScaleDenominator>2321428.571428572</ScaleDenominator>
<TopLeftCorner>2420000.0 1350000.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>3</MatrixWidth>
<MatrixHeight>2</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ScaleDenominator>1785714.285714286</ScaleDenominator>
<TopLeftCorner>2420000.0 1350000.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>4</MatrixWidth>
<MatrixHeight>3</MatrixHeight>
</TileMatrix>
<TileMatrix>

<ScaleDenominator>892857.142857143</ScaleDenominator>
<TopLeftCorner>2420000.0 1350000.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>8</MatrixWidth>
<MatrixHeight>5</MatrixHeight>
</TileMatrix>
<TileMatrix>

<ScaleDenominator>357142.85714285716</ScaleDenominator>
<TopLeftCorner>2420000.0 1350000.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>19</MatrixWidth>
<MatrixHeight>13</MatrixHeight>
</TileMatrix>
<TileMatrix>

<ScaleDenominator>178571.42857142858</ScaleDenominator>
<TopLeftCorner>2420000.0 1350000.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>38</MatrixWidth>
<MatrixHeight>25</MatrixHeight>
</TileMatrix>
<TileMatrix>

<ScaleDenominator>71428.57142857143</ScaleDenominator>
<TopLeftCorner>2420000.0 1350000.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>94</MatrixWidth>
<MatrixHeight>63</MatrixHeight>
</TileMatrix>
<TileMatrix>

<ScaleDenominator>35714.28571428572</ScaleDenominator>
<TopLeftCorner>2420000.0 1350000.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>188</MatrixWidth>
<MatrixHeight>125</MatrixHeight>
</TileMatrix>
<TileMatrix>

<ScaleDenominator>17857.14285714286</ScaleDenominator>
<TopLeftCorner>2420000.0 1350000.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>375</MatrixWidth>
<MatrixHeight>250</MatrixHeight>
</TileMatrix>
<TileMatrix>

<ScaleDenominator>8928.57142857143</ScaleDenominator>
<TopLeftCorner>2420000.0 1350000.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>750</MatrixWidth>
<MatrixHeight>500</MatrixHeight>
</TileMatrix>
<TileMatrix>

<ScaleDenominator>7142.857142857143</ScaleDenominator>
<TopLeftCorner>2420000.0 1350000.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>938</MatrixWidth>
<MatrixHeight>625</MatrixHeight>
</TileMatrix>
<TileMatrix>

<ScaleDenominator>5357.142857142858</ScaleDenominator>
<TopLeftCorner>2420000.0 1350000.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>1250</MatrixWidth>
<MatrixHeight>834</MatrixHeight>
</TileMatrix>
<TileMatrix>

<ScaleDenominator>3571.4285714285716</ScaleDenominator>
<TopLeftCorner>2420000.0 1350000.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>1875</MatrixWidth>
<MatrixHeight>1250</MatrixHeight>
</TileMatrix>
<TileMatrix>

<ScaleDenominator>1785.7142857142858</ScaleDenominator>
<TopLeftCorner>2420000.0 1350000.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>3750</MatrixWidth>
<MatrixHeight>2500</MatrixHeight>
</TileMatrix>
<TileMatrix>

<ScaleDenominator>892.8571428571429</ScaleDenominator>
<TopLeftCorner>2420000.0 1350000.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>7500</MatrixWidth>
<MatrixHeight>5000</MatrixHeight>
</TileMatrix>
<TileMatrix>

<ScaleDenominator>357.14285714285717</ScaleDenominator>
<TopLeftCorner>2420000.0 1350000.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>18750</MatrixWidth>
<MatrixHeight>12500</MatrixHeight>
</TileMatrix>
</TileMatrixSet>"""

python_dict = xml_to_dict(xml_data)
print(repr(python_dict))