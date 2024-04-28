from utils import gps

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
