from app.wmts.utils import BBox


def get_wms_params(bbox: BBox, layers: str, gutter:int, width:int=256, height:int=256, image_format:str='png'):
    return {
        'SERVICE': 'WMS',
        'VERSION': '1.3.0',
        'REQUEST': 'GetMap',
        'FORMAT': f'image/{image_format}',
        'TRANSPARENT': 'true' if image_format == 'png' else 'false',
        'LAYERS': layers,
        'WIDTH': f'{width + (gutter * 2)}',
        'HEIGHT': f'{height + (gutter * 2)}',
        'CRS': f'EPSG:2056',
        'STYLES': '',
        #'TIME': request.view_args['time'],
        'BBOX': ','.join([str(b) for b in bbox.bbox])
    }


def get_wms_resource(bbox, gutter, width=256, height=256):
    params = get_wms_params(bbox, gutter, width, height)
    return get_wms_image(settings.WMS_BACKEND, params)
