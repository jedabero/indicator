import signal
import gi
from subprocess import check_output

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk
from gi.repository import AppIndicator3
from gi.repository import Notify

APP_ID = 'com.jedabero.indicator'


def app_test(_):
    out = check_output(['./test.sh'])
    Notify.Notification.new('Output', out.decode(), None).show()


def app_quit(_):
    Notify.uninit()
    Gtk.main_quit()


def build_menu():
    menu = Gtk.Menu()
    item_test = Gtk.MenuItem('Ejecutar script')
    item_test.connect('activate', app_test)
    menu.append(item_test)
    item_quit = Gtk.MenuItem('Salir')
    item_quit.connect('activate', app_quit)
    menu.append(item_quit)
    menu.show_all()
    return menu


def main():
    indicator = AppIndicator3.Indicator.new(APP_ID, Gtk.STOCK_EXECUTE, AppIndicator3.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    Notify.init(APP_ID)
    Gtk.main()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
