#!/usr/bin/env python
from rich.layout import Layout, Splitter, RowSplitter, ColumnSplitter, NoSplitter

class ZanotabLayout(Layout):
    """ Supports a list of layouts to be split """

    zano_splitters = {"column": RowSplitter, "row": ColumnSplitter, RowSplitter: ColumnSplitter, ColumnSplitter: RowSplitter}

    def __init__(self, nested_list=None, *args, splitter="row", **kwargs):
        # print("reached with", nested_list)
        # splitter = kwargs.pop("splitter", self.splitters["column"]())
        # if isinstance(splitter, str):
            # splitter = self.splitters[splitter]()
        # print("splitter", splitter)

        if isinstance(nested_list, list):
            super().__init__(*args, **kwargs)
            # reverse splitter!
            try:
                self.splitter = self.zano_splitters[splitter]()
            except KeyError:
                self.splitter = self.zano_splitters[splitter.name]()
            # print("splitter", self.splitter)
            self.split(*nested_list)#splitter=splitter)
        else:
            super().__init__(nested_list, *args, **kwargs)
            self.splitter = self.splitters[splitter]().name
            # self.splitter = self.zano_splitters[splitter.name]()

    def _layout_select(self, layout):
        if isinstance(layout, Layout):
            return layout
        # if isinstance(layout, list):
            # mode = self.splitter.name
            # return ZanotabLayout([ZanotabLayout(i) for i in layout]) # something else?
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


# layout = ZanotabLayout( [
    # Layout(name="header", size=1),
    # [Layout(ratio=1, name="main"), Layout(ratio=1, name="maini2"), Layout(ratio=3, name="main3")],
    # Layout(size=10, name="footer"),
#  ])

# layout['body'].update(layout.tree)


# layout["main"].split_row(
#         Layout(name="body", ratio=2),
#         Layout(name="side")
#         )

# layout["side"].split(Layout(name="memory"), Layout(name="results"))

# layout["body"].update(
#     Align.center(
#         Text(
#             """This is a demonstration of rich.Layout\n\nHit Ctrl+C to exit""",
#             justify="center",
#         ),
#         vertical="middle",
#     )
# )

# -----------------------------------------------------
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

    if __name__ == "__main__":
        with live:
            try:
                while True:
                    sleep(1)
            except KeyboardInterrupt:
                pass
