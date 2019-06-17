import uuid

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QWidget

from helpers.inspection_helpers import has_method


# Value used to determine if a setting does not exist. Its uniqueness should ensure we do not ignore any settings.
NOT_FOUND_VALUE = uuid.uuid4()


def save_widget(store: QSettings, widget: QWidget, group: str):
    """ Store all layout aspects of a widget. Checks to see if save_state is available too. """
    store.beginGroup(group)
    # noinspection PyBroadException
    try:
        if has_method(widget, "saveState") and has_method(widget, "restoreState"):
            store.setValue("state", widget.saveState())

        store.setValue("geometry", widget.saveGeometry())
        store.setValue("is_maximised", widget.isMaximized())
    except Exception:
        # Do not prevent continuing to load the program if settings appear invalid
        pass
    finally:
        store.endGroup()


def restore_widget(store: QSettings, widget: QWidget, group: str):
    """ Restore a widget based on its previous state. """
    store.beginGroup(group)
    # noinspection PyBroadException
    try:
        if has_method(widget, "saveState") and has_method(widget, "restoreState"):
            state = store.value("state", NOT_FOUND_VALUE)
            if state != NOT_FOUND_VALUE:
                widget.restoreState(state)

        geometry = store.value("geometry", NOT_FOUND_VALUE)
        if geometry != NOT_FOUND_VALUE:
            widget.restoreGeometry(geometry)

        is_maximised: str = store.value("is_maximised", NOT_FOUND_VALUE)
        if is_maximised != NOT_FOUND_VALUE and is_maximised.lower() == "true":
            widget.showMaximized()
        else:
            widget.showNormal()
    except Exception:
        # Do not prevent continuing to load the program if settings appear invalid
        pass
    finally:
        store.endGroup()