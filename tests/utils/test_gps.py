import pytest

from utils import gps

def test_pitch_image_offset():
    assert gps.pitch_image_offset() == (-60, 1860, -29, 1189)

def test_get_color_from_speed():
    assert gps.get_color_from_speed(5.2) == [236, 218, 154]
    assert gps.get_color_from_speed(5.41) == [239, 196, 126]
    assert gps.get_color_from_speed(5.6) == [239, 196, 126]
    assert gps.get_color_from_speed(5.81) == [243, 173, 106]
    assert gps.get_color_from_speed(6.0) == [243, 173, 106]
    assert gps.get_color_from_speed(6.21) == [247, 148, 93]
    assert gps.get_color_from_speed(6.4) == [247, 148, 93]
    assert gps.get_color_from_speed(6.61) == [249, 123, 87]
    assert gps.get_color_from_speed(6.8) == [249, 123, 87]
    assert gps.get_color_from_speed(7.01) == [246, 99, 86]
    assert gps.get_color_from_speed(7.2) == [246, 99, 86]
    assert gps.get_color_from_speed(7.41) == [238, 77, 90]
    assert gps.get_color_from_speed(7.6) == [238, 77, 90]

def test_distance_and_bearing():
    lat1, lon1, lat2, lon2 = 63.445152, 10.450687, 63.444589, 10.452373
    d, b = gps.distance_and_bearing(lat1, lon1, lat2, lon2)
    assert d == 104.61172932214025
    assert b == 126.75680552701871

    lat3, lon3 = 63.445640, 10.451500
    d2, b2 = gps.distance_and_bearing(lat1, lon1, lat3, lon3)
    assert d2 == 67.65938702776376
    assert b2 == 36.677596149528995

def test_local_coordinates():
    assert gps.local_coordinates(100, 0) == (0, 100)
    assert gps.local_coordinates(100, 45) == pytest.approx((70.71067811865476, 70.71067811865476))
    assert gps.local_coordinates(100, 90) == pytest.approx((100, 0))

def test_find_pitch():
    lat, lon = 63.44523733, 10.45186
    # the result is a dictionary, and we also need approximate values
    result = gps.find_pitch(lat, lon)
    assert result['bearing'] == pytest.approx(36.677596149528995)
    assert result['length'] == pytest.approx(104.61172932214025)
    assert result['width'] == pytest.approx(67.65938702776376)
    assert result['lat'] == [63.445152, 63.44564, 63.445077, 63.444589]
    assert result['lon'] == [10.450687, 10.4515, 10.453186, 10.452373]

    # sometimes the pitch is not found
    assert gps.find_pitch(1, 2) == None

def test_equirectangular():
    assert gps.equirectangular(63.44523733, 10.45186) == (519562.93536337535, 7054798.476810544)

    assert gps.equirectangular(59.9172961, 10.8068681) == (602336.846308802, 6662508.756366668)

def test_rotate_coordinates():
    assert gps.rotate_coordinates(100, 0, 0) == (100, 0)
    assert gps.rotate_coordinates(100, 0, 90) == pytest.approx((0, 100))
    assert gps.rotate_coordinates(100, 0, 180) == pytest.approx((-100, 0))
    assert gps.rotate_coordinates(100, 0, 270) == pytest.approx((0, -100))

    assert gps.rotate_coordinates(100, 0, 30) == pytest.approx((86.60254037844386, 50))
    assert gps.rotate_coordinates(100, 100, 30) == pytest.approx((36.602540378443884, 136.60254037844388))
    assert gps.rotate_coordinates(100, 100, 180) == pytest.approx((-100, -100))
    assert gps.rotate_coordinates(100, 100, 360) == pytest.approx((100, 100))
    assert gps.rotate_coordinates(100, 100, 580) == pytest.approx((-12.325683343243782, -140.88320528055175))
    assert gps.rotate_coordinates(0, 100, 300) == pytest.approx((86.60254037844386, 50))

    assert gps.rotate_coordinates(0, -100, 90) == pytest.approx((100, 0))

def test_wgs84_to_wm():
    assert gps.wgs84_to_wm(48.137154, 11.576124) == (1288648.2290397931, 6129702.780250119)
    assert gps.wgs84_to_wm(63.44523733, 10.45186) == (1163495.7330425843, 9210266.292824231)

    assert gps.wgs84_to_wm(63.445152, 10.450687) == (1163365.1552798839, 9210245.045056127)
    assert gps.wgs84_to_wm(63.445640, 10.451500) == (1163455.6580258987, 9210366.561331064)

    assert gps.wgs84_to_wm(59.917296, 10.806868) == (1203015.0428301226, 8381347.728534192)

def test_wgs84_to_utm():
    assert gps.wgs84_to_utm(47.9941214, 7.8509671) == (414278.1673102494, 5316285.594923587)

    assert gps.wgs84_to_utm(63.44523733, 10.45186) == (572413.5047751537, 7036018.568816292)

    assert gps.wgs84_to_utm(63.445152, 10.450687) == (572355.2226412792, 7036007.737140305)
    assert gps.wgs84_to_utm(63.445640, 10.451500) == (572394.5348316443, 7036063.020347464)

    assert gps.wgs84_to_utm(59.917296, 10.806868) == (601026.0227616715, 6643579.264003792)
