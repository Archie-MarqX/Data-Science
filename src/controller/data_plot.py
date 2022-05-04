# Import libraries
import matplotlib.pyplot as plt
import pandas as pd


class DataPlot:
    class DataPlotConfig:
        title = ""
        axis_X = ""
        axis_Y = ""
        data = pd.DataFrame()

        def set_Title(self, title):
            self.title = title
            return self

        def set_Axis_X_Name(self, axis_X):
            self.axis_X = axis_X
            return self

        def set_Axis_Y_Name(self, axis_Y):
            self.axis_Y = axis_Y
            return self

        def set_dataFrame(self, data):
            self.data = data
            return self

    def simple_Plot(self, dataPlotConfig: DataPlotConfig):
        try:
            plt.figure(figsize=(26.66667 * 0.75, 15 * 0.75))
            plt.plot(
                dataPlotConfig.data,
                label="Ativo",
                alpha=0.75,
                linewidth=2,
                color="blue",
            )
            plt.hlines(
                0,
                min(dataPlotConfig.data.index.values),
                max(dataPlotConfig.data.index.values),
            )
            y = dataPlotConfig.data.values
            plt.vlines(dataPlotConfig.data.idxmax(), 0, dataPlotConfig.data.max())
            plt.title(dataPlotConfig.title)
            plt.legend(loc="lower right")
            plt.ylim(min(y), max(y))
            plt.xlim(min(dataPlotConfig.data.index), max(dataPlotConfig.data.index))
            plt.xlabel(dataPlotConfig.axis_X)
            plt.ylabel(dataPlotConfig.axis_Y)
            plt.grid("True")
            plt.show()
        except Exception as e:
            print("[Error]: " + str(e))

    def complex_Plot(self, dataPlotConfig: DataPlotConfig):
        dateList = []

        for element in dataPlotConfig.data.index:
            month = str(element.month)
            year = str(element.year)
            if len(month) == 1 and month.startswith("1"):
                dateList.append(str(year))
            elif (
                month.startswith("3") or month.startswith("6") or month.startswith("9")
            ):
                dateList.append(month)
            else:
                dateList.append(None)

        axis_X = dateList
        # create an index for each tick position
        tick_X = list(range(len(axis_X)))
        y = dataPlotConfig.data.values * 100

        plt.figure(figsize=(26.66667, 15))
        plt.plot(tick_X, y, marker="o", color="b", label="Retorno")
        plt.ylim(min(y), max(y))
        plt.xlim(min(tick_X), max(tick_X))
        plt.xlabel(dataPlotConfig.axis_X)
        plt.ylabel(dataPlotConfig.axis_Y)
        plt.xticks(tick_X, axis_X)
        plt.title(dataPlotConfig.title)
        plt.legend()
        plt.grid(True, axis="both")
        plt.show()
