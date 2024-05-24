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

def test_local_coordinates_for_two_points():
    lat1, lon1 = 63.44523733, 10.45186
    lat2, lon2 = 63.44517933, 10.452014
    assert gps.local_coordinates_for_two_points(lat1, lon1, lat2, lon2) == (41.09733383696133, 42.43931498114769, 51.08926705078824, 41.839736236557286, 67.65938702776376, 104.61172932214025, 36.677596149528995)

def test_local_coordinates_for_point():
    lat, lon = 63.44523733, 10.45186
    assert gps.local_coordinates_for_point(lat, lon) == (41.09733383696133, 42.43931498114769, 67.65938702776376, 104.61172932214025, 36.677596149528995)

    assert gps.local_coordinates_for_point(59.9172961, 10.8068681) == (0.012435724990500689, -0.00024856453259149597, 67.72861736817303, 104.99316291959485, 295.4772229067301)

    assert gps.local_coordinates_for_point(59.9175581, 10.8057711) == (0.012435700662525683, 67.72836863686541, 67.72861736817303, 104.99316291959485, 295.4772229067301)

    assert gps.local_coordinates_for_point(59.91841, 10.80657) == (104.68129213085548, 68.2773462389974, 67.72861736817303, 104.99316291959485, 295.4772229067301)

    assert gps.local_coordinates_for_point(59.91814, 10.8076) == (102.27204755827937, 3.5385884500755878, 67.72861736817303, 104.99316291959485, 295.4772229067301)
