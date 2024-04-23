from threading import Event
from concurrent.futures import ThreadPoolExecutor
from DeviceMonitor import DeviceMonitor
import time
from ConfigurationLoader import ConfigLoader
from DeviceLogger import DeviceLogger

shutdown_event = Event()

def main_loop(devices, wkst_logger, external_handler=None):
    wkst_logger.warning("Entering device monitor loop.")
    with ThreadPoolExecutor(max_workers=len(devices)) as executor:
        futures = [executor.submit(DeviceMonitor(device, shutdown_event, external_handler).connect_and_monitor) for device in devices]

        while not all(future.done() for future in futures):
            time.sleep(0.1)  # Adjust as necessary to reduce busy waiting

        if shutdown_event.is_set():
            wkst_logger.warning("Shutdown event is set. Breaking loop.")

    wkst_logger.warning("All threads have been cleanly shutdown.")

def start_monitoring(text_handler=None):
    config_loader = ConfigLoader()
    devices = config_loader.get_devices()
    config = config_loader.get_configuration()
    # Pass the text_handler to get_logger
    wkst_logger = DeviceLogger.get_logger("workstation", config['output_dir'], None, config['log_format'], external_handler=text_handler)
    main_loop(devices, wkst_logger, text_handler)


def stop_monitoring():
    shutdown_event.set()
