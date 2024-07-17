import pandas as pd
import matplotlib.pyplot as plt
import os

class PlotDrawer:
    def __init__(self, plots_dir='plots'):
        self.plots_dir = plots_dir
        if not os.path.exists(plots_dir):
            os.makedirs(plots_dir)

    def draw_plots(self, json_file):
        # Загрузка данных из JSON файла
        df = pd.read_json(json_file)
        print(df.head())  # Вывод первых 5 строк DataFrame для проверки структуры данных
        plot_paths = []

        # Преобразование всех столбцов, кроме 'name', в числовой формат
        for col in df.columns:
            if col != 'name':
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Создание графиков для каждого столбца, кроме 'name'
        for col in df.columns:
            if col != 'name':
                plt.figure()
                df.plot(kind='bar', x='name', y=col)
                plt.title(f'{col} Comparison')
                plt.xlabel('Room')
                plt.ylabel('Degrees')
                plt.xticks(rotation=45)
                plt.tight_layout()
                plot_path = os.path.join(self.plots_dir, f'{col}.png')
                plt.savefig(plot_path)
                plt.close()
                plot_paths.append(plot_path)

        return plot_paths

if __name__ == '__main__':
    json_file = 'deviation.json'
    drawer = PlotDrawer()
    plot_paths = drawer.draw_plots(json_file)
    if plot_paths:
        print(f'Plots saved in directory: {drawer.plots_dir}')
        print('Paths to plots:')
        for path in plot_paths:
            print(path)
    else:
        print('Failed to generate plots.')
