

MEMORY_LOCATION = "memory@any"


def memory_repository(packages):
    from allzpark import _rezapi as rez

    manager = rez.package_repository_manager
    repository = manager.get_repository(MEMORY_LOCATION)
    repository.data = packages


def wait(signal, on_value=None, timeout=1000):
    from allzpark.vendor.Qt import QtCore

    loop = QtCore.QEventLoop()
    state = {"timeout": True}

    if on_value:
        def trigger(value):
            if value == on_value:
                loop.quit()
                state["timeout"] = False
    else:
        def trigger(*args):
            loop.quit()
            state["timeout"] = False

    signal.connect(trigger)

    QtCore.QTimer.singleShot(timeout, loop.quit)
    loop.exec_()

    if state["timeout"]:
        raise Exception("Signal waiting timeout.")
