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
    label = Gtk.Label(out.decode())
    win = Gtk.Window(title="Resultado")
    win.add(label)
    win.show_all()
    """Notify.Notification.new('Output', out.decode(), None).show()"""


def app_quit(_):
    Notify.uninit()
    Gtk.main_quit()


def make_menu(text, callback):
    item_test = Gtk.MenuItem(text)
    item_test.connect('activate', callback)
    return item_test


def build_menu():
    menu = Gtk.Menu()
    menu.append(make_menu('Ejecutar script', app_test))
    menu.append(make_menu('Salir', app_quit))
    """
    submenuitem = Gtk.MenuItem('Submenu')
    submenu = Gtk.Menu()
    submenu.append(make_menu('Ejecutar script', app_test))
    submenuitem.set_submenu(submenu)
    menu.append(submenuitem)
    """
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
