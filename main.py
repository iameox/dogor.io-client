import sys

from Application import Application

if __name__ == '__main__':
    app = Application()
    app.setup()

    sys.exit(app.exec())
