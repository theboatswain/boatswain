from PyQt5.QtWidgets import QTableView


class UniformRowHeights(QTableView):
    """
    ref https://stackoverflow.com/questions/4031168/qtableview-is-extremely-slow-even-for-only-3000-rows
    by implement sizeHintForRow will improve the scrolling's performance
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._row_height = None

    def sizeHintForRow(self, row):
        model = self.model()
        if row < 0 or row >= model.rowCount():
            # Mirror super implementation.
            return -1
        return self.getRowHeight()

    def getRowHeight(self):
        if self._row_height is None:
            self._row_height = max(self.getCellHeights())
        return self._row_height

    def changeEvent(self, event):
        # This for instance happens when the style sheet changed. It may affect
        # the calculated row height. So invalidate:
        self._row_height = None
        super().changeEvent(event)

    def getCellHeights(self, row=0):
        self.ensurePolished()
        option = self.viewOptions()
        model = self.model()
        for column in range(model.columnCount()):
            index = model.index(row, column)
            delegate = self.itemDelegate(index)
            if delegate:
                yield delegate.sizeHint(option, index).height()
