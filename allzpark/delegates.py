from .vendor.Qt import QtWidgets, QtCore


class Package(QtWidgets.QStyledItemDelegate):

    editor_created = QtCore.Signal()
    editor_closed = QtCore.Signal(bool)

    def __init__(self, ctrl, parent=None):
        super(Package, self).__init__(parent)

        def on_close_editor(*args):
            self.editor_closed.emit(self._changed)
        self.closeEditor.connect(on_close_editor)

        self._changed = True
        self._default = None
        self._ctrl = ctrl

    def createEditor(self, parent, option, index):
        if index.column() != 1:
            return

        editor = QtWidgets.QComboBox(parent)

        def on_text_activated(text):
            self._changed = text == self._default
        editor.textActivated.connect(on_text_activated)

        return editor

    def setEditorData(self, editor, index):
        model = index.model()
        options = model.data(index, "versions")
        default = index.data(QtCore.Qt.DisplayRole)

        editor.addItems(options)
        editor.setCurrentIndex(options.index(default))
        self._default = default
        self.editor_created.emit()

    def setModelData(self, editor, model, index):
        model = index.model()
        package = model.data(index, "family")
        options = model.data(index, "versions")
        default = model.data(index, "default")
        version = options[editor.currentIndex()]

        if not version or version == default:
            return
        # has changed
        self._ctrl.patch("%s==%s" % (package, version))
