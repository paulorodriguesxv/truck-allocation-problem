import pytest
import app
from optimizer import SmartOptimizer


class TestApp:
    """ App integration test suit """

    def test_display(self):
        """
        Test case for display function
        """
        op = SmartOptimizer()
        op.load('trucks.csv', 'cargo.csv')

        df_distance, row_ind, col_ind = op.optimizer()

        app.display_result(df_distance, row_ind, col_ind)
