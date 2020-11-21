import pytest
import pandas as pd
from optimizer import SmartOptimizer
from exceptions import DataNotLoadedError, InvalidDataSizeError


class DataSet():
    def get_truck(self):
        return pd.DataFrame(
            [["Hartford Plastics Incartford", "Florence", "AL", 34.79981, -87.677251],
            ["Beyond Landscape & Design Llcilsonville",	"Fremont", "CA", 37.5482697, -121.9885719],
            ["Ibrahim Chimandalpharetta", "Toledo",	"OH", 41.6639383, -83.55521200000001]],
            columns=["truck", "city", "state", "lat", "lng"])
    
    def get_cargo(self):
        return pd.DataFrame([["Light bulbs", "Sikeston", "MO",	
                                36.876719, -89.5878579, "Grapevine",	
                                "TX", 32.9342919, -97.0780654],
                                ["Recyclables", "Christiansburg", "VA",	
                                37.1298517, -80.4089389,	"Apopka",
                                "FL",28.6934076, -81.5322149]],
                                columns=["product", "origin_city", "origin_state", "origin_lat",	
                                "origin_lng",	"destination_city",	"destination_state", 
                                "destination_lat", "destination_lng"])



@pytest.fixture(scope="module")
def dataset():
    return DataSet()

class TestOptimizer:
    """ GeospatialUtils integration test suit """


    def test_data_loaded(self):
        """
        Test case for check if data was loaded
        """
        opt = SmartOptimizer()
        opt.load('trucks.csv', 'cargo.csv')        

        assert (opt._is_data_loaded())

    def test_data_size(self):
        """
        Test case for check the size of dataset
        """
        opt = SmartOptimizer()
        opt.load('trucks.csv', 'cargo.csv')        

        assert (opt._is_valid_data_size())

    def test_data_not_loaded(self):
        """
        Test case for check correct handling when data is not loaded
        """
        with pytest.raises(DataNotLoadedError):
            opt = SmartOptimizer()
            opt._validate_data_files()     

    def test_data_invalid_size(self):
        """
        Test case for check correct handling when data size is not valid
        """
        with pytest.raises(InvalidDataSizeError):
            opt = SmartOptimizer()
            opt.load('trucks_invalid_size.csv', 'cargo.csv')
            opt._validate_data_files()

    def test_transform_quadratic_matrix(self, dataset):
        """
        Test case for check quadratic matrix generator
        """
        trucks = dataset.get_truck()
        cargo = dataset.get_cargo()

        cargo["product_city"] = cargo["product"] + "_" + \
            cargo["origin_city"] + "_" + cargo["destination_city"]

        df_distances = pd.DataFrame(
                index=[trucks["truck"]],
                columns=[cargo["product_city"]])

        opt = SmartOptimizer()
        df_distances = opt._transform_quadratic_matrix(df_distances, trucks, cargo)
        
        assert df_distances.shape == (3, 3)

    def test_build_cost_matrix(self, dataset):
        """
        Test case for check build cost matrix
        """
        trucks = dataset.get_truck()
        cargo = dataset.get_cargo()

        opt = SmartOptimizer()
        df = opt._build_cost_matrix(trucks, cargo)

        info = df.loc["Hartford Plastics Incartford", "Light bulbs_Sikeston_Grapevine"]
        assert round(info.values[0][0]) == 288

    def test_build_cost_matrix(self, dataset):
        """
        Test case for check build cost matrix
        """
        opt = SmartOptimizer()
        opt.load('trucks.csv', 'cargo.csv')        

        row_ind_resp = [ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16,
            17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
            34, 35, 36, 37, 38, 39, 40, 41, 42, 43]
        col_ind_resp = [34, 31, 27, 23, 15, 12, 13, 14,  0, 16, 17, 18, 19, 20, 21, 22,  4,
            24, 25, 26,  5, 28, 29, 30,  1, 32, 33,  2, 35, 36, 37, 38, 39, 40,
            41, 42, 43, 11, 10,  9,  8,  7,  6,  3]

        df_distance, row_ind, col_ind = opt.optimizer()

        assert (sum(row_ind_resp - row_ind) == 0)
        assert (sum(col_ind_resp - col_ind) == 0)


