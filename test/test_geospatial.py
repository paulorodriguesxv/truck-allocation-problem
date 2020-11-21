import pytest
from geospatial import GeospatialUtils


class TestGeoSpatialUtils:
    """ GeospatialUtils integration test suit """

    #def setUp(self):
    #    self.geo_utils = SmartOptimizer()

    def test_calculate_distance(self):
        """
        Test case for calculate_distance function
        """
        new_york = dict(lat=40.71278, lng=-74.00594)
        los_angeles = dict(lat=34.05223, lng=-118.24368)
        city_distance = 3937

        geo_d = GeospatialUtils()
        distance = geo_d.calculate_distance(new_york, los_angeles)
        
        assert (round(distance) == city_distance)

