import atexit
import logging
import sys
import loop_handler
import util
import util.process
from time import sleep
from os.path import isfile
from globals import status
from pypresence import InvalidID
from settings import local_settings
from wrappers import system_tray_icon
from util.updates import check_version_and_download
from util.log_setup import setup_logging


# From https://stackoverflow.com/a/16993115/8286014
def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt) or issubclass(exc_type, SystemExit):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logging.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = handle_exception


def reload():
    global status
    logging.info("Reloading...")

    try:
        tray_icon.discord_rp.exit_rp()
    except (RuntimeError, AttributeError, AssertionError, InvalidID):
        pass
    except NameError:
        return

    status = status.DISABLED
    loop_handler.reload_lastfm()
    status = status.ENABLED


def close_app(icon=None, item=None):
    global status
    logging.info("Closing app...")

    try:
        tray_icon.discord_rp.exit_rp()
    except (RuntimeError, AttributeError, AssertionError, InvalidID):
        pass

    tray_icon.tray_icon.stop()
    status = status.KILL

    if not loop_handler.sc.empty():
        logging.debug(f"Closing {len(loop_handler.sc.queue)} events...")
        for event in loop_handler.sc.queue:
            loop_handler.sc.cancel(event)


def open_settings_and_wait():
    util.process.open_settings()
    # Starting the process takes a bit, if we went straight into the next while block, the method would
    # finish immediately because "settings_ui" is not running.
    while not util.process.check_process_running("settings_ui"):
        pass

    while util.process.check_process_running("settings_ui"):
        sleep(1.5)


if __name__ == "__main__":
    setup_logging("main")
    atexit.register(close_app)

    if util.process.check_process_running("discord_fm"):
        logging.info("Discord.fm is already running!")
        close_app()

    if util.updates.check_version_and_download():
        logging.info("Quitting to allow installation of newer version")
        close_app()

    if not isfile(util.resource_path(".env")):
        logging.critical(".env file not found, unable to get API keys and data!")
        close_app()

    if util.arg_exists("-o"):
        logging.info("\"-o\" argument was found, opening settings")
        util.process.open_settings()

    if local_settings.first_load:
        logging.info("First load, opening settings UI and waiting for it to be closed...")
        open_settings_and_wait()

    no_username = local_settings.get("username") == ""
    if no_username and not util.is_frozen():
        logging.critical("No username found - please add a username to settings and restart the app")
        close_app()
    elif no_username and util.is_frozen():
        logging.info("No username found, opening settings UI and waiting for it to be closed...")
        open_settings_and_wait()

    tray_icon = system_tray_icon.SystemTrayIcon(close_app)

    try:
        loop_handler = loop_handler.LoopHandler(tray_icon)
        loop_handler.handle_update()
    except (KeyboardInterrupt, SystemExit):
        close_app()

    sys.exit()
