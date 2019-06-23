from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QDesktopWidget


def size_from_percentage_of_screen(width: float, height: float) -> QSize:
    """
    Get a size based on the percentage of the screen you want to occupy.
    Width and height are floats between 0 and 1, with 1 being 100% of the available space.
    """
    if width < 0:
        width = 0
    if height < 0:
        height = 0
    if width > 100:
        width = 100
    if height > 100:
        height = 100

    size = QDesktopWidget().availableGeometry().size()
    return QSize(int(size.width() * width), int(size.height() * height))


def centre_on_screen(widget: QWidget):
    """ Centre the given widget on the screen, regardless of where the parent window frame is. """

    # Get the widget's frame size.
    widget_frame = widget.frameGeometry()

    # Get the centre of the screen.
    screen_centre = QDesktopWidget().availableGeometry().center()

    # Calculate where the frame should be placed.
    widget_frame.moveCenter(screen_centre)

    # Move the widget to the correct place.
    widget.move(widget_frame.topLeft())
