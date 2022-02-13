import atexit
import logging
import sys
import loop_handler
import util
import globals
import util.process
from time import sleep
from os.path import isfile
from pypresence import InvalidID
from settings import local_settings
from wrappers import system_tray_icon
from util.updates import check_version_and_download


class AppManager:
    def __init__(self):
        self.tray_icon = system_tray_icon.SystemTrayIcon(self.close)
        self.loop = loop_handler.LoopHandler(self.tray_icon)

    def start(self):
        atexit.register(globals.manager.close)

        if util.process.check_process_running("discord_fm") and not util.arg_exists("--ignore-open"):
            logging.info("Discord.fm is already running!")
            self.close()

        if util.updates.check_version_and_download() and not util.is_frozen():
            logging.info("Quitting to allow installation of newer version")
            self.close()

        if not isfile(util.resource_path(".env")):
            logging.critical(".env file not found, unable to get API keys and data!")
            self.close()

        if util.arg_exists("-o"):
            logging.info("\"-o\" argument was found, opening settings")
            open_settings_and_wait()
        elif local_settings.first_load:
            logging.info("First load, opening settings UI and waiting for it to be closed...")
            open_settings_and_wait()

        no_username = local_settings.get("username") == ""
        if no_username and not util.is_frozen():
            logging.critical("No username found - please add a username to settings and restart the app")
            self.close()
        elif no_username and util.is_frozen():
            logging.info("No username found, opening settings UI and waiting for it to be closed...")
            open_settings_and_wait()

        try:
            self.loop.handle_update()
        except (KeyboardInterrupt, SystemExit):
            self.close()
        except ValueError:
            self.close()
            util.basic_notification("Invalid username",
                                    "Please open Discord.fm Settings to change to a valid username.")

        sys.exit()

    def reload(self):
        logging.info("Reloading...")

        try:
            self.tray_icon.discord_rp.exit_rp()
        except (RuntimeError, AttributeError, AssertionError, InvalidID):
            pass
        except NameError:
            return

        globals.current = globals.Status.DISABLED
        self.loop.reload_lastfm()
        globals.current = globals.Status.ENABLED

    def close(self):
        logging.info("Closing app...")
        globals.current = globals.Status.KILL

        try:
            self.tray_icon.discord_rp.exit_rp()
            self.tray_icon.tray_icon.stop()
        except (RuntimeError, AttributeError, AssertionError, InvalidID, NameError):
            pass

        try:
            sc = self.loop.sc
            if not sc.empty():
                for event in sc.queue:
                    sc.cancel(event)
                    logging.debug(f"Event \"{event.action}\" canceled")
        except (AttributeError, NameError):
            pass

        sys.exit()


def open_settings_and_wait():
    util.process.open_settings()
    # Starting the process takes a bit, if we went straight into the next while block, the method would
    # finish immediately because "settings_ui" is not running.
    while not util.process.check_process_running("settings_ui"):
        pass

    while util.process.check_process_running("settings_ui"):
        sleep(1.5)