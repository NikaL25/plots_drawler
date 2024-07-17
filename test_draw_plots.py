import unittest
import os
import pandas as pd
from draw_plots import PlotDrawer

class TestPlotDrawer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.json_file = 'deviation.json'
        cls.drawer = PlotDrawer()
        cls.test_plots_dir = 'test_plots'
        cls.drawer.plots_dir = cls.test_plots_dir
        if not os.path.exists(cls.test_plots_dir):
            os.makedirs(cls.test_plots_dir)

        cls.df = pd.read_json(cls.json_file)

    def test_json_file_exists(self):
        self.assertTrue(os.path.exists(self.json_file))

    def test_load_json(self):
        df = pd.read_json(self.json_file)
        self.assertIsInstance(df, pd.DataFrame)

    def test_column_names(self):

        expected_columns = ['name', 'gt_corners', 'rb_corners', 'mean', 'max', 'min',
                            'floor_mean', 'floor_max', 'floor_min',
                            'ceiling_mean', 'ceiling_max', 'ceiling_min']
        self.assertTrue(set(expected_columns).issubset(self.df.columns))


    def test_plot_content(self):
        plot_paths = self.drawer.draw_plots(self.json_file)
        for path in plot_paths:
            self.assertGreater(os.path.getsize(path), 0)

    @classmethod
    def tearDownClass(cls):
        for root, dirs, files in os.walk(cls.test_plots_dir):
            for file in files:
                os.remove(os.path.join(root, file))
        os.rmdir(cls.test_plots_dir)

if __name__ == '__main__':
    unittest.main()
