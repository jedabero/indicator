import signal
import gi
from os import listdir
from os.path import isfile, join, dirname, splitext
from subprocess import check_output

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk, Gdk
from gi.repository import AppIndicator3
from gi.repository import Notify

APP_ID = 'com.jedabero.indicator'


def exec(_, script):
    # Buscar la carpeta de scripts
    path = join(dirname(__file__), 'scripts')
    # Ejecutar el script
    out = check_output([path + '/' + script])
    show_script_result(script, out.decode())


def show_script_result(script_name, output):
    label = Gtk.Label(output)
    win = Gtk.Window(title="Resultado " + script_name)
    scroll = Gtk.ScrolledWindow()
    scroll.add(label)
    win.add(scroll)
    win.show_all()
    # Obtener tamaño posible del resultado
    size = label.size_request()
    # Obtener tamaño de la pantalla actual
    screen = Gdk.Screen.get_default()
    monitor = screen.get_monitor_at_window(screen.get_active_window())
    geometry = screen.get_monitor_geometry(monitor)
    if size.width < geometry.width or size.height < geometry.height:
        # Redimensionar si el tamaño posible es menor que el espacio disponible
        win.resize(size.width, size.height)
    else:
        # Maximizar cuando el output sea muy grande
        win.maximize()
    Notify.Notification.new('Done ' + script_name, "Script " + script_name + " ended execution", None).show()


def app_quit(_):
    Notify.uninit()
    Gtk.main_quit()


def make_menu(text, callback, arg=None):
    item_test = Gtk.MenuItem(text)
    if arg:
        item_test.connect('activate', callback, arg)
    else:
        item_test.connect('activate', callback)
    return item_test


def build_menu():
    menu = Gtk.Menu()
    path = join(dirname(__file__), 'scripts')
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    submenuitem = Gtk.MenuItem('Scripts')
    submenu = Gtk.Menu()
    for script in onlyfiles:
        script_name, _ = splitext(script)
        submenu.append(make_menu(script_name.replace("_", " ").capitalize(), exec, script))
        submenuitem.set_submenu(submenu)
    menu.append(submenuitem)
    menu.append(make_menu('Salir', app_quit))
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
