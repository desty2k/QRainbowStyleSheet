from qtpy import QtCore, QtWidgets




def getWorkspace() -> QtCore.QRect:
    """Returns workspace area"""
    return QtWidgets.QApplication.desktop().availableGeometry()





