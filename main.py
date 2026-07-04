# main.py
import sys
import time

from PyQt6.QtWidgets import QApplication

from lib.ui.ui_setting_loader import UISettingsLoader
from lib.ui.window import MainWindowCA

loop_status_on = True
def main_loop(engine):
    global loop_status_on

    while loop_status_on:
        if not engine.any_checklist_active:
            engine.try_auto_activate()
            time.sleep(30)
        else:
            # checklist attiva → aspetta risposte vocali
            time.sleep(0.1)

def stop_all():
    global loop_status_on
    loop_status_on = False
    print("[SYSTEM] Loop stopped")

def load_checklist_and_start():
    print("[SYSTEM] Speech manager started")
    try:
        main_loop(engine)
    except KeyboardInterrupt:
        stop_all(speech)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    settings = UISettingsLoader()
    w = MainWindowCA(settings)
    w.show()
    sys.exit(app.exec())