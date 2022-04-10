import numpy as np
import timeit


class TestBase:

    def MSE(self, c1, c2):
        """
        Mean Squared Error Calculation

        :param c1:
        :param c2:
        :return:
        """

        assert len(c1) == len(c2), f"Columns need to be same dimensions, c1:{len(c1)}, c2:{len(c2)}"

        _n = len(c1)
        _mse = np.round((((c1 - c2)**2).sum())/_n, 5)

        return _mse

    def run(self, test_set):
        print("Running test set ", test_set)
        for test in test_set:
            print("Running test case: ", test)
            _t0 = timeit.default_timer()
            _func = getattr(self, f"test_case_{test}")()
            _t1 = timeit.default_timer()
            if _func:
                print(f"Test case {test} PASSED")
            else:
                print(f"Test case {test} FAILED")
            _delta_time = _t1 - _t0
            print('execution time [s]', np.round(_delta_time,3))


