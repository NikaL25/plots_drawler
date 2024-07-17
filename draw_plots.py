import pandas as pd
import matplotlib.pyplot as plt
import os
import cProfile

class PlotDrawer:
    def __init__(self, plots_dir='plots_dir'):
        self.plots_dir = plots_dir
        if not os.path.exists(plots_dir):
            os.makedirs(plots_dir)

    def draw_plots(self, json_file):
        try:
            df_index = pd.read_json(json_file, orient='index')
            df_index = df_index.apply(pd.to_numeric, errors='coerce', axis=1)
            df_index['name'] = df_index.index
            print("df_index:")
            print(df_index.head())

            df_standard = pd.read_json(json_file)
            for col in df_standard.columns:
                if col != 'name':
                    df_standard[col] = pd.to_numeric(df_standard[col], errors='coerce')

            plot_paths = []

            # Создание графиков для данных с ориентацией index
            for col in df_index.columns:
                if col != 'name':
                    plot_path = os.path.join(self.plots_dir, f'{col}_index.png')
                    df_index.plot(kind='bar', x='name', y=col)
                    plt.title(f'{col} Comparison (Index)')
                    plt.xlabel('Room')
                    plt.ylabel('Degrees')
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    plt.savefig(plot_path)
                    plt.close()
                    plot_paths.append(plot_path)


            for col in df_standard.columns:
                if col != 'name':
                    plot_path = os.path.join(self.plots_dir, f'{col}_standard.png')
                    df_standard.plot(kind='bar', x='name', y=col)
                    plt.title(f'{col} Comparison (Standard)')
                    plt.xlabel('Room')
                    plt.ylabel('Degrees')
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    plt.savefig(plot_path)
                    plt.close()
                    plot_paths.append(plot_path)

            print(f"Generated {len(plot_paths)} plots")
            return plot_paths

        except ValueError as e:
            print(f"ValueError: {e}")
            return []
        except FileNotFoundError as e:
            print(f"FileNotFoundError: {e}")
            return []

def main():
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

if __name__ == '__main__':
    cProfile.run('main()', 'profile_output.prof')
