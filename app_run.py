import subprocess
import sys
import os
from threading import Thread
import time

def run_kedro():
    """Запускает Kedro pipeline."""
    print("Запуск Kedro...")
    subprocess.run(["kedro", "run"], check=True)

def run_gui():
    """Запускает GUI."""
    print("Запуск GUI...")
    
    src_path = os.path.join(os.path.dirname(__file__), "src")
    sys.path.append(src_path)

    from SUML_PowerCast_App.pipelines.app_run.gui.GUI import App
    app = App()
    app.mainloop()

if __name__ == "__main__":
    kedro_thread = Thread(target=run_kedro)
    kedro_thread.start()

    time.sleep(15)

    run_gui()

    kedro_thread.join()