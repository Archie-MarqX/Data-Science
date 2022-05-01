# Import libraries
import matplotlib.pyplot as plt
import pandas as pd


class DataPlot:
    class DataPlotConfig:
        title = ""
        axisX = ""
        axisY = ""
        data = pd.DataFrame()

        def set_Title(self, title):
            self.title = title
            return self

        def set_Axis_X_Name(self, axisX):
            self.axisX = axisX
            return self

        def set_Axis_Y_Name(self, axisY):
            self.axisY = axisY
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
            plt.vlines(dataPlotConfig.data.idxmax(), 0, dataPlotConfig.data.max())
            plt.title(dataPlotConfig.title)
            plt.legend(loc="lower right")
            plt.xlabel(dataPlotConfig.axisX)
            plt.ylabel(dataPlotConfig.axisY)
            plt.show()
        except Exception as e:
            print("[Error]: " + str(e))


# dataPlot    = DataPlot
# config      = dataPlot.DataPlotConfig().setAxisX('Data').setAxisY('Retorno em %').setTitle('Title').setData(df)
# dataPlot.simplePlot(config)
