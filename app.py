"""
It's requires python 3.6.

This cargo x trucks problem belongs to a quadratic assignment problem
category and was solved using hungarian algorithm minimization allocation,
using scipy lib for calculation. The algorithm build steps was documented
at notebook called backend-test.ipynb.

    To install dependencies:
        pip install pipenv
        cd loadsmart
        pipenv update

    To run app:
        cd loadsmart
        pipenv shell
        python app.py

    To run jupyter notebook
        cd loadsmart
        pipenv shell
        jupyter notebook backend-test.ipynb

    To run tests:
        cd loadsmart
        pipenv shell
        python -m pytest -vv -s --cov=. --cov-report xml:coverage/coverage.xml --cov-report term-missing .
"""

from pandas import DataFrame
from optimizer import SmartOptimizer
from tabulate import tabulate


def display_result(df_distance: DataFrame,
                   row_ind: list,
                   col_ind: list) -> None:
    """ display final result

    :param df_distance: dataframe with distance matrix
        from each truck to each cargo origin position

    :param row_ind: row with best fit

    :param col_ind: col with best fit
    """

    TRUCK_IDX = 0
    CARGO_IDX = 1

    print("Optimal mapping of trucks to cargos table")
    print("-----------------------------------------")

    data = []
    for item in zip(row_ind, col_ind):
        distance = df_distance.iloc[item[TRUCK_IDX], item[CARGO_IDX]]
        if distance == 0:
            continue

        truck_name = df_distance.iloc[item[TRUCK_IDX]].name
        product_name, origin, destination = \
            df_distance.iloc[:, item[CARGO_IDX]].name.split("_")

        data.append([truck_name,
                     product_name,
                     origin,
                     destination,
                     distance])

    print(tabulate(data, headers=['Truck', 'Cargo',
                                  'Origin', 'Destination',
                                  'Distance from origin (km)']))
    print("-----------------------------------------")

    # cost_matrix = df_distance.astype('float').values
    # cost = cost_matrix[row_ind, col_ind].sum()
    # print(f"Total distance is {cost:.2f} km")


if __name__ == "__main__":
    op = SmartOptimizer()
    op.load('trucks.csv', 'cargo.csv')

    df_distance, row_ind, col_ind = op.optimizer()

    display_result(df_distance, row_ind, col_ind)
