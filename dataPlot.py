import matplotlib.pyplot    as  plt

class DataPlot:
    def simplePlot(self, data, title, x='Data', y='USD'):
        plt.figure(figsize=(26.66667 * 0.75, 15 * 0.75))
        plt.plot(data, label="Ativo", alpha=0.75, linewidth=2, color="blue")
        plt.hlines(0, min(data.index.values), max(data.index.values))
        plt.vlines(data.idxmax(), 0, data.max())
        plt.title(title)
        plt.legend(loc="lower right")
        plt.xlabel(x)
        plt.ylabel(y)
        plt.show()