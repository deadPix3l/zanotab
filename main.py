#!/usr/bin/env python
from rich.layout import Layout, Splitter, RowSplitter, ColumnSplitter, NoSplitter

class ZanotabLayout(Layout):
    """ Supports a list of layouts to be split """

    zano_splitters = {"column": RowSplitter, "row": ColumnSplitter, RowSplitter: ColumnSplitter, ColumnSplitter: RowSplitter}

    def __init__(self, nested_list=None, *args, splitter="row", **kwargs):

        if isinstance(nested_list, list):
            super().__init__(*args, **kwargs)
            # reverse splitter!
            try:
                self.splitter = self.zano_splitters[splitter]()
            except KeyError:
                self.splitter = self.zano_splitters[splitter.name]()
            self.split(*nested_list)#splitter=splitter)
        else:
            super().__init__(nested_list, *args, **kwargs)
            self.splitter = self.splitters[splitter]().name

    def _layout_select(self, layout):
        if isinstance(layout, Layout):
            return layout

        return ZanotabLayout(layout, splitter=self.splitter)

    def split(self, *layouts) -> None:
        """Split the layout in to multiple sub-layouts.

        Args:
            *layouts (Layout): Positional arguments should be (sub) Layout instances.
            splitter (Union[Splitter, str]): Splitter instance or name of splitter.
        """
        _layouts = [
            self._layout_select(layout) for layout in layouts
        ]

        self._children[:] = _layouts

if __name__ == "__main__":
    from rich.live import Live
    from time import sleep
    layout = ZanotabLayout([
        Layout(name="header", size=5),
        [Layout(ratio=1, name="body"), Layout(ratio=1, name="side")],
        [ZanotabLayout(name="main"), [ZanotabLayout(size=10, name="footer"), [Layout(), Layout(), Layout(name="footer2")]]],
        ZanotabLayout(name="main2")
        ]
        )

    live = Live(layout, screen=True, redirect_stderr=False)
    with live:
        try:
            while True:
                sleep(1)
        except KeyboardInterrupt:
            pass
