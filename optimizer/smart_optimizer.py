import pandas as pd
from scipy.optimize import linear_sum_assignment
from exceptions import DataNotLoadedError, InvalidDataSizeError
from geospatial import GeospatialUtils


class SmartOptimizer():
    """ This class aim to provide a way to find the optimal mapping of
    trucks and cargos to minimize the overall distances the trucks must
    travel​.

    .. warning::
        For this class work well, you MUST to be two csv files.

            1) File with cargos:
            columns:
                product
                origin_city
                origin_state
                origin_lat
                origin_lng
                destination_city
                destination_state
                destination_lat
                destination_lng

            2) File with trucks:
            columns:
                truck
                city
                state
                lat
                lng
    """

    def __init__(self):
        self._trucks = None
        self._cargo = None

    def _is_data_loaded(self) -> bool:
        return (self._trucks is not None) and (self._cargo is not None)

    def _is_valid_data_size(self) -> bool:
        return len(self._cargo) <= len(self._trucks)

    def _validate_data_files(self):
        """ execute validations for data files """
        if not self._is_data_loaded():
            raise DataNotLoadedError

        if not self._is_valid_data_size():
            raise InvalidDataSizeError("Cargo list have to be smaller "
                                       "than trucks list")

    def _calculate_distance(self, point1: dict, point2: dict) -> float:
        utils = GeospatialUtils()
        return utils.calculate_distance(point1, point2)

    def _transform_quadratic_matrix(self,
                                    df: pd.DataFrame,
                                    trucks: pd.DataFrame,
                                    cargo: pd.DataFrame) -> pd.DataFrame:
        """ transform a retangular matrix into a new quadratic matrix
            by generating fake columns with zero value

        :param df: **df**.
            pandas dataframe with distances list

        :param trucks: **trucks dataframe**.
            pandas dataframe with trucks list

        :param cargo: **cargo dataframe**.
            pandas dataframe with cargo list

        :return: quadratic dataframe matrix
        """
        fake_columns_count = len(trucks) - len(cargo) + 1

        for i in range(1, fake_columns_count):
            df[f'fake{i}'] = pd.Series(0, index=df.index)

        return df

    def _build_cost_matrix(self, trucks: pd.DataFrame,
                           cargo: pd.DataFrame) -> pd.DataFrame:
        """ build the cost matrix for hungarian algorithm
        the cost matrix is based in distance (km)

        :param trucks: **trucks dataframe**.
            pandas dataframe with trucks list

        :param cargo: **cargo dataframe**.
            pandas dataframe with cargo list

        :return: cost matrix (dataframe)
        """

        cargo["product_city"] = cargo["product"] + "_" + \
            cargo["origin_city"] + "_" + cargo["destination_city"]

        df_distances = pd.DataFrame(0,
                index=trucks["truck"],
                columns=cargo["product_city"].values)

        for _, truck_row in trucks.iterrows():
            for _, product_row in cargo.iterrows():

                distance = self._calculate_distance(
                    dict(lat=truck_row['lat'],
                         lng=truck_row['lng']),
                    dict(lat=product_row['origin_lat'],
                         lng=product_row['origin_lng'])
                    )

                df_distances.loc[truck_row['truck'],
                                 product_row['product_city']] = distance

        # because hungarian algorithm need a quadratic matrix
        df_distances = self._transform_quadratic_matrix(
            df_distances, trucks, cargo)

        return df_distances

    def load(self, truck_filename: str, cargo_filename: str):
        """ load csv data files """
        self._trucks = pd.read_csv(truck_filename)
        self._cargo = pd.read_csv(cargo_filename)

    def optimizer(self):
        """ Optimize the allocation for all trucks and cargos relations

        :return: cost matrix (dataframe)
                 row indices corresponding column indices giving the optimal assignment
                 col indices corresponding column indices giving the optimal assignment
        """

        self._validate_data_files()

        df_distance = self._build_cost_matrix(self._trucks, self._cargo)
        cost_matrix = df_distance.astype('float').values

        row_ind, col_ind = linear_sum_assignment(cost_matrix)

        return df_distance, row_ind, col_ind
