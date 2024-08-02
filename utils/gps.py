import base64
from io import BytesIO
from itertools import product
import math
from PIL import Image
import requests
from typing import Dict, Iterable, Tuple

import numpy as np
from pyproj import Geod, Transformer
import streamlit as st

def image_to_base64(image_path, image_format):
    '''
    Convert an image to base64 format.

    Parameters:
    image_path (str): The path to the image.
    image_format (str): The format of the image.

    Returns:
    str: The image in base64 format.
    '''
    pil_image = Image.open(image_path)
    image_file = BytesIO()
    pil_image.save(image_file, format=image_format)
    image_base64 = base64.b64encode(image_file.getvalue()).decode()

    return f'data:image/{image_format};base64,{image_base64}'

def pitch_image_offset():
    '''
    The image of the football pitch (assets/pitch.png) is 1920x1218 pixels. The image contains some area around the pitch, so the actual pitch area is smaller. The position of the actual pitch is 1800x1160 pixels, centered in the image.
            image start,    pitch start,    pitch end,  image end
    width   0,              60,             1860,       1920
    height  0,              29,             1189,       1218

    Returns:
    tuple: The offset of the pitch image to the full image (x1, x2, y1, y2).
    '''
    image_width = 1920
    image_height = 1218
    pitch_width = 1800
    pitch_height = 1160

    x1 = - (image_width - pitch_width) // 2
    x2 = x1 + image_width
    y1 = - (image_height - pitch_height) // 2
    y2 = y1 + image_height

    return x1, x2, y1, y2

def pitch_image_extent(length, width):
    '''
    Consider the pitch image offset in pixels and the actual pitch length and width in meters, calculate the extent of the pitch image in meters.

    Pitches may have different lengths and widths, so the pitch image may be stretched or compressed to fit the actual pitch size.

    Parameters:
    length (float): The length of the pitch in meters.
    width (float): The width of the pitch in meters.

    Returns:
    tuple: The extent of the pitch image in meters (x1, x2, y1, y2).
    '''
    x1, x2, y1, y2 = pitch_image_offset()

    x_ratio = (x1 + x2) / length
    x1_m = x1 / x_ratio
    x2_m = x2 / x_ratio
    y_ratio = (y1 + y2) / width
    y1_m = y1 / y_ratio
    y2_m = y2 / y_ratio

    return x1_m, x2_m, y1_m, y2_m

def get_pitches():
    # latitude and longitude of the 4 corners of football pitches
    # the order is bottom left, top left, top right, bottom right (clockwise from bottom left) when the pitch is displayed as a rectangle with the long side horizontal
    # the bottom left corner will be used as the base point (0, 0) for calculating the local coordinates of other points on the pitch, so it is important to get the correct order
    pitch_coordinates = [
        {
            'lat': [63.445152, 63.445640, 63.445078, 63.444589],
            'lon': [10.450687, 10.451500, 10.453188, 10.452373]
        },
        # {
        #     'lat': [38.709955, 38.709013, 38.709006, 38.709948],
        #     'lon': [-9.264591, -9.264576, -9.265357, -9.265371]
        # },
        # {
        #     'lat': [59.965881, 59.964977, 59.964963, 59.965872],
        #     'lon': [10.727593, 10.727629, 10.726449, 10.726415]
        # },
        # {
        #     'lat': [59.921578, 59.920727, 59.920978, 59.921829],
        #     'lon': [10.582160, 10.581354, 10.580300, 10.581107]
        # },
        # {
        #     'lat': [60.425951, 60.425341, 60.425449, 60.426058],
        #     'lon': [5.472725, 5.472585, 5.470686, 5.470826]
        # },
        # {
        #     'lat': [60.425952, 60.425342, 60.425342, 60.426059],
        #     'lon': [5.472727, 5.472581, 5.470827, 5.470827]
        # },
        {
            'lat': [60.426013, 60.426304, 60.425514, 60.425223],
            'lon': [5.304449, 5.305454, 5.306391, 5.305386]
        },
        # {
        #     'lat': [60.425952, 60.425341, 60.425446, 60.426059],
        #     'lon': [5.472728, 5.472587, 5.470685, 5.470827]
        # },
        {
            'lat': [59.917296, 59.917558, 59.918411, 59.918148],
            'lon': [10.806868, 10.805771, 10.806579, 10.807680]
        },
        # {
        #     'lat': [58.776009, 58.775089, 58.774953, 58.775876],
        #     'lon': [5.633550, 5.633943, 5.632799, 5.632397]
        # },
        # {
        #     'lat': [60.159541, 60.158628, 60.158465, 60.159378],
        #     'lon': [10.266314, 10.266817, 10.265632, 10.265129]
        # },
        # {
        #     'lat': [59.068927, 59.068083, 59.067886, 59.068731],
        #     'lon': [10.037055, 10.037652, 10.036601, 10.036004]
        # },
        # {
        #     'lat': [63.412718, 63.412112, 63.411963, 63.412569],
        #     'lon': [10.405404, 10.405620, 10.403541, 10.403325]
        # },
        # {
        #     'lat': [59.920812, 59.920321, 59.920830, 59.921322],
        #     'lon': [10.584996, 10.584336, 10.582837, 10.583499]
        # },
        # {
        #     'lat': [59.921436, 59.920977, 59.921600, 59.922060],
        #     'lon': [10.805464, 10.804661, 10.803248, 10.804051]
        # },
        # {
        #     'lat': [59.942162, 59.941299, 59.941457, 59.942321],
        #     'lon': [10.635737, 10.635261, 10.634157, 10.634633]
        # },
        # {
        #     'lat': [63.445078, 63.444588, 63.445150, 63.445641],
        #     'lon': [10.453189, 10.452374, 10.450683, 10.451499]
        # },
        # # pitches without clear boundaries
        # {
        #     'lat': [37.189091, 37.188148, 37.188007, 37.188958],
        #     'lon': [-7.418629, -7.418332, -7.419032, -7.419331]
        # }
    ]

    return pitch_coordinates

def in_pitch(lat, long):
    '''
    Check if the latitude and longitude are inside any football pitch.

    Parameters:
    lat (float): The latitude.
    long (float): The longitude.

    Returns:
    bool: True if the coordinates are inside any football pitch, False otherwise.
    '''
    pitch_coordinates = get_pitches()

    for pitch in pitch_coordinates:
        if (lat >= min(pitch['lat']) and lat <= max(pitch['lat'])) and (long >= min(pitch['lon']) and long <= max(pitch['lon'])):
            return True

    return False

def distance_and_bearing(lat1, lon1, lat2, lon2):
    '''
    Given the latitude and longitude of two points, calculate the distance and initial bearing from the first point to the second point.

    Parameters:
    lat1 (float): The latitude of the first point.
    lon1 (float): The longitude of the first point.
    lat2 (float): The latitude of the second point.
    lon2 (float): The longitude of the second point.
    All latitudes and longitudes are in decimal degrees, with positive values indicating north and east, and negative values indicating south and west. Example: 63.444589, 10.452373

    Returns:
    tuple: The distance and bearing between the two points.
    Distance is in meters.
    Bearing is in degrees, measured clockwise from true north (0-360, 0 is true north). Example: 306.7583
    '''
    # use WGS84 ellipsoid to calculate the distance and bearing, the most common ellipsoid for GPS data
    geod = Geod(ellps="WGS84")
    # note the parameters required by PROJ are lon first!
    b, _, d = geod.inv(lon1, lat1, lon2, lat2)

    return d, b

def local_coordinate(distance, bearing):
    '''
    Given the distance and bearing, calculate the local coordinates of a point relative to the base point (0, 0).
    Parameters:
    distance (float): The distance from the base point, in meters.
    bearing (float): The bearing from the base point, in degrees (0-360, 0 is true north)

    Returns:
    tuple: The local coordinates (x, y) of the point from the base point, in meters.
    '''
    # use basic trigonometry to calculate the local coordinates
    x = distance * math.sin(math.radians(bearing))
    y = distance * math.cos(math.radians(bearing))

    return x, y

def find_pitch(lat: float, lon: float) -> Dict:
    '''
    Find the pitch that contains the latitude and longitude, and return the pitch or None if the coordinates are not inside any pitch.

    Parameters:
    lat (float): The latitude.
    lon (float): The longitude.

    Returns:
    dict: The pitch that contains the latitude and longitude.
    '''
    pitch_coordinates = get_pitches()

    for pitch in pitch_coordinates:
        if (lat >= min(pitch['lat']) and lat <= max(pitch['lat'])) and (lon >= min(pitch['lon']) and lon <= max(pitch['lon'])):
            break
    else:
        return None

    # the base point is the bottom left corner of the pitch
    # width is the distance from the bottom left corner to the top left corner
    # the rotation angle is the bearing from the bottom left corner to the top left corner
    width, bearing = distance_and_bearing(pitch['lat'][0], pitch['lon'][0], pitch['lat'][1], pitch['lon'][1])
    # length is the distance from the bottom left corner to the bottom right corner
    length, _ = distance_and_bearing(pitch['lat'][0], pitch['lon'][0], pitch['lat'][3], pitch['lon'][3])

    pitch['width'] = width
    pitch['length'] = length
    pitch['bearing'] = bearing

    # center of the pitch
    pitch['center'] = (np.mean(pitch['lat']), np.mean(pitch['lon']))

    return pitch

def equirectangular(lat, lon):
    '''
    convert the lat and lon data to cartesian coordinates using equirectangular projection

    Parameters:
    lat (float): latitude
    lon (float): longitude
    All latitudes and longitudes are in decimal degrees, with positive values indicating north and east, and negative values indicating south and west. Example: 63.444589, 10.452373

    Returns:
    tuple: The cartesian coordinates (x, y)
    '''
    # radius of the Earth in meters
    R = 6371009
    # convert the lat and lon data to radians
    lat = np.radians(lat)
    lon = np.radians(lon)
    # convert the lat and lon data to cartesian coordinates (latitude is y, longitude is x)
    x = R * lon * np.cos(lat)
    y = R * lat

    return x, y

def rotate_coordinate(x, y, angle_degrees):
    '''
    Rotate the coordinates by the given angle. The rotation is counter-clockwise.

    Parameters:
    x (float): The x-coordinate.
    y (float): The y-coordinate.
    angle_degrees (float): The angle to rotate the coordinates, in degrees.

    Returns:
    tuple: The rotated coordinates (x, y).
    '''
    angle = math.radians(angle_degrees)
    x_rotated = x * math.cos(angle) - y * math.sin(angle)
    y_rotated = x * math.sin(angle) + y * math.cos(angle)

    return x_rotated, y_rotated

@st.cache_data()
def convert_coordinates(
    lat_col: Iterable[float],
    lon_col: Iterable[float],
    method: str
) -> Tuple[
        Tuple[Tuple[float, ...], Tuple[float, ...]],  # x and y coordinates
        dict,  # pitch info
    ]:

    '''
    Takes two columns of latitude and longitude and returns the converted coordinates that can be used for plotting on a uniform football pitch.

    Parameters:
    lat_col (list-like): The column of latitude values.
    lon_col (list-like): The column of longitude values.
    method (str): The method to convert the coordinates. Options:
        - 'equirectangular': equirectangular projection
        - 'distance_bearing': distance and bearing based calculations. Slower.
        - 'WebMercator': Web Mercator projection (often used in online maps)
        - 'utm': UTM (Universal Transverse Mercator) projection

    Returns:
    tuple: The converted x and y coordinates, and the pitch info. Or None if the pitch is not found.
    '''
    # use the first point to find the pitch
    pitch = find_pitch(lat_col.iloc[0], lon_col.iloc[0])
    if pitch is None:
        return None
    angle = pitch['bearing']
    base_point = (pitch['lat'][0], pitch['lon'][0])

    if method == 'equirectangular':
        # use equirectangular projection to convert the lat and lon to x and y
        coords = [equirectangular(lat, lon) for lat,lon in zip(lat_col, lon_col)]
        # x and y are relative to the base point
        base_x, base_y = equirectangular(*base_point)
        coords = [(x - base_x, y - base_y) for x, y in coords]
        # rotate the coordinates
        coords = [rotate_coordinate(x, y, angle) for x, y in coords]

    elif method == 'distance_bearing':
        # find the distance and bearing from the base point to the point
        distance_col, bearing_col = zip(*[distance_and_bearing(*base_point, lat, lon) for lat, lon in zip(lat_col, lon_col)])
        # calculate the coordinates of the point relative to the base point on the pitch
        coords = [local_coordinate(d, b - angle) for d, b in zip(distance_col, bearing_col)]

    elif method == 'WebMercator':
        # Web Mercator projection, often used in online maps
        coords = [wgs84_to_wm(lat, lon) for lat, lon in zip(lat_col, lon_col)]
        # x and y are relative to the base point
        base_x, base_y = wgs84_to_wm(*base_point)
        coords = [(x - base_x, y - base_y) for x, y in coords]
        # rotate the coordinates
        coords = [rotate_coordinate(x, y, angle) for x, y in coords]

    elif method == 'utm':
        # convert from WGS84 (GPS) to UTM (Universal Transverse Mercator)
        # find the UTM zone for the base point
        epsg = utm_zone(*base_point)
        # convert the lat and lon data to UTM coordinates
        # always_xy=True ensures the function returns in the order of x, y
        transformer = Transformer.from_crs("EPSG:4326", epsg, always_xy=True)
        # note the parameters required by PROJ are lon first!
        coords = [transformer.transform(lon, lat) for lat, lon in zip(lat_col, lon_col)]
        # x and y are relative to the base point
        base_x, base_y = transformer.transform(base_point[1], base_point[0])
        coords = [(x - base_x, y - base_y) for x, y in coords]
        # rotate the coordinates
        coords = [rotate_coordinate(x, y, angle) for x, y in coords]

    x_col, y_col = zip(*coords)
    return (x_col, y_col), pitch

def wgs84_to_wm(
    lat: float,
    lon: float,
) -> Tuple[float, float]:
    '''
    Convert from WGS84 (GPS coordinates) to Web Mercator (coordinates used in online maps).
    '''
    # always_xy=True ensures the function returns in the order of x, y
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
    # note the parameters required by PROJ are lon first!
    # the current function is lat first to be consistent with the rest of the code
    x, y = transformer.transform(lon, lat)

    # Mercator projection needs a scale factor at high latitudes
    # but even with the scale factor, the result is still quite off
    # scale_factor = math.cos(math.radians(lat))
    # x *= scale_factor
    # y *= scale_factor

    return x, y

def utm_zone(
    lat: float,
    lon: float,
) -> str:
    '''
    Find the UTM zone for the given latitude and longitude and return the EPSG code for the UTM zone.
    '''
    # the UTM zone for the given latitude and longitude, including zones in Svalbard and northern Norway
    zone = int((lon + 180) // 6) + 1
    if lat >= 56 and lat < 64 and lon >= 3 and lon < 12:
        zone = 32
    elif lat >= 72 and lat < 84:
        if lon >= 0 and lon < 9:
            zone = 31
        elif lon >= 9 and lon < 21:
            zone = 33
        elif lon >= 21 and lon < 33:
            zone = 35
        elif lon >= 33 and lon < 42:
            zone = 37
    # the EPSG code for the UTM zone
    epsg = f"EPSG:326{zone}"
    # for the southern hemisphere, the EPSG code is 327xx
    if lat < 0:
        epsg = f"EPSG:327{zone}"

    return epsg

def fetch_sat_img(
    lat_deg: float,
    lon_deg: float
) -> Tuple[
    Image.Image,
    Tuple[float, float, float, float]
]:
    '''
    Given latitude and longitude (in decimal degrees), return the satellite image that cover the area, and the extent of the image in latitude and longitude.
    '''
    # zoom level
    zoom = 17
    # get the tile numbers that cover the area
    tiles = get_tile_numbers(lat_deg, lon_deg, zoom)
    xmin, xmax, ymin, ymax = tiles['xmin'], tiles['xmax'], tiles['ymin'], tiles['ymax']

    # full size image to add the tiles to
    tile_size = 256
    img = Image.new('RGB',
                    ((xmax - xmin + 1) * tile_size, (ymax - ymin + 1) * tile_size))

    # loop through every tile inside the bounding box
    for x, y in product(range(xmin, xmax + 1), range(ymin, ymax + 1)):
        tile = fetch_tile(x, y, zoom)
        # paste the tile into the full image
        img.paste(tile, ((x - xmin) * tile_size, (y - ymin) * tile_size))

    # crop the image to the area around the point
    # add some padding around the point
    x_padding = 0.0016
    y_padding = 0.0007
    lat_min = lat_deg - y_padding
    lat_max = lat_deg + y_padding
    lon_min = lon_deg - x_padding
    lon_max = lon_deg + x_padding
    # the pixel coordinates of the corners of the cropped image
    x1, y1 = latlon_to_pixel(lat_max, lon_min, zoom, tile_size)
    x2, y2 = latlon_to_pixel(lat_min, lon_max, zoom, tile_size)

    # the arguments are relative to the top left corner
    img = img.crop((
        x1 - xmin * tile_size,
        y1 - ymin * tile_size,
        x2 - xmin * tile_size,
        y2 - ymin * tile_size
    ))

    # the extent of the cropped image in latitude and longitude
    extent = (lon_min, lon_max, lat_min, lat_max)

    return img, extent

def latlon_to_tile(
    lat_deg: float,
    lon_deg: float,
    zoom: int,
) -> Tuple[float, float]:
    '''
    Given latitude and longitude (in decimal degrees) and a zoom level, return the point in the tile numbering system (with fractional part).
    '''
    # see https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    x = (lon_deg + 180.0) / 360.0 * n
    y = (1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n

    return x, y

def latlon_to_pixel(
    lat_deg: float,
    lon_deg: float,
    zoom: int,
    tile_size: int,
) -> Tuple[int, int]:
    '''
    Given latitude and longitude (in decimal degrees), a zoom level, and the size of a tile, return the pixel coordinates of the point
    '''
    xpoint, ypoint = latlon_to_tile(lat_deg, lon_deg, zoom)
    x = int(xpoint * tile_size)
    y = int(ypoint * tile_size)

    return x, y

def get_tile_numbers(lat_deg: float, lon_deg: float, zoom: int) -> Dict[str, int]:
    '''
    Given latitude and longitude (in decimal degrees) and a zoom level, return the tile numbers that cover the area (can be multiple tiles).
    '''
    xpoint, ypoint = latlon_to_tile(lat_deg, lon_deg, zoom)

    # the tile numbers of the point
    xtile = int(xpoint)
    ytile = int(ypoint)

    # the fractional part of the tile numbers
    xfrac = xpoint - xtile
    yfrac = ypoint - ytile

    # if the point is near the edge of a tile, get nearby tiles as well, so the whole area can be displayed
    threshold = 0.45
    # the bounding box of the tiles
    xmin = xtile
    xmax = xtile
    ymin = ytile
    ymax = ytile

    if xfrac < threshold:
        xmin -= 1
    if yfrac < threshold:
        ymin -= 1

    if xfrac > 1 - threshold:
        xmax += 1
    if yfrac > 1 - threshold:
        ymax += 1

    # limit the number of tiles to prevent accidental large downloads
    assert (xmax - xmin + 1) * (ymax - ymin + 1) <= 9, 'Too many tiles to download'

    # return a dictionary
    tiles = {
        'xmin': xmin,
        'xmax': xmax,
        'ymin': ymin,
        'ymax': ymax
    }

    return tiles

@st.cache_data()
def fetch_tile(x: int, y: int, zoom: int) -> Image.Image:
    '''
    Fetch one tile of the satellite image from online providers like Mapbox.
    x and y are the tile numbers, and zoom is the zoom level.
    '''
    # mapbox access token
    token = st.secrets['mapbox']['token']

    # the URL for the satellite image from Mapbox
    path = 'https://api.mapbox.com/v4/mapbox.satellite/'
    url = f'{path}{zoom}/{x}/{y}.jpg?access_token={token}'

    # make the request
    resp = requests.get(url)
    resp.raise_for_status()
    image = Image.open(BytesIO(resp.content))

    return image
