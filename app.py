from PyQt6.QtWidgets import QApplication, QWidget

# Only needed for access to command line arguments
import sys


class App:
    def __init__(self):
        self.app = QApplication(sys.argv)

        # Create a Qt widget, which will be our window.
        self.window = QWidget()

    def run(self):
        self.window.show()  # IMPORTANT!!!!! Windows are hidden by default.

        # Start the event loop.
        self.app.exec()

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.


# Your application won't reach here until you exit and the event
# loop has stopped.
