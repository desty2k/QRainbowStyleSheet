import os
import sys


if sys.platform == "win32" and not os.getenv("FORCE_NON_WIN"):
    from .FramelessWindowWin import FramelessWindow
    import logging
    logging.getLogger().info("Imported frameless windows with Windows API support")
else:
    from .FramelessWindow import FramelessWindow

from .FramelessMessageBox import (FramelessWarningMessageBox, FramelessQuestionMessageBox,
                                  FramelessInformationMessageBox, FramelessCriticalMessageBox, FramelessMessageBox)  # noqa
