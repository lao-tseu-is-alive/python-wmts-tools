def get_wms_params(bbox, gutter, width=256, height=256, image_format = 'png'):

    return {
        'SERVICE': 'WMS',
        'VERSION': '1.3.0',
        'REQUEST': 'GetMap',
        'FORMAT': f'image/{image_format}',
        'TRANSPARENT': 'true' if image_format == 'png' else 'false',
        #'LAYERS': request.view_args["layer_id"],
        'WIDTH': f'{width + gutter * 2}',
        'HEIGHT': f'{height + gutter * 2}',
        #'CRS': f'EPSG:{request.view_args["srid"]}',
        'STYLES': '',
        #'TIME': request.view_args['time'],
        'BBOX': ','.join([str(b) for b in bbox])
    }

def get_wms_resource(bbox, gutter, width=256, height=256):
    params = get_wms_params(bbox, gutter, width, height)
    logger.debug(
        'Fetching wms image: %s?%s',
        settings.WMS_BACKEND,
        '&'.join([f'{k}={v}' for k, v in params.items()])
    )
    return get_wms_image(settings.WMS_BACKEND, params)

