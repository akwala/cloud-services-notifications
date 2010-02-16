import pygtk
pygtk.require('2.0')
import gtk
from cloudsn.core import config
from cloudsn.ui import preferences
from cloudsn.core.indicator import Indicator
from cloudsn.const import *
import gettext

class StatusIconIndicator (Indicator):

    def set_active(self, active):
        if active:
            self.statusIcon = gtk.StatusIcon()
            self.statusIcon.set_from_pixbuf(config.get_cloudsn_icon())
            self.statusIcon.set_visible(True)
            self.statusIcon.set_tooltip(APP_LONG_NAME)
            self.statusIcon.connect('activate', self.main_cb, self.statusIcon)

            self.menu = self.create_pref_menu()        
            self.indmenu = self.create_main_menu()

            self.statusIcon.connect('popup-menu', self.popup_menu_cb, self.menu)
            self.statusIcon.set_visible(1)
        else:
            #TODO Discable the indicators
            logger.debug("deactivate Not implemented")

    def get_name(self):
        return _("Status Icon")

    def create_main_menu(self):
        indmenu = gtk.Menu()
        indmenuItem = gtk.MenuItem("")
        indmenuItem.get_child().set_markup("<b>%s</b>" % (APP_LONG_NAME))
        indmenuItem.connect('activate', self.quit_cb, self.statusIcon)
        indmenuItem.set_sensitive(False)
        indmenu.append(indmenuItem)

        return indmenu

    def create_pref_menu(self):
        menu = gtk.Menu()
        menuItem = gtk.ImageMenuItem(gtk.STOCK_PREFERENCES)
        menuItem.connect('activate', self.preferences_cb, self.statusIcon)
        menu.append(menuItem)
        menuItem = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        menuItem.connect('activate', self.quit_cb, self.statusIcon)
        menu.append(menuItem)
        return menu
        
    def create_indicator(self, acc):
        indmenuItem = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        pix = acc.get_provider().get_icon().scale_simple(16,16,gtk.gdk.INTERP_BILINEAR)
        
        """
        indmenuItem.set_image(gtk.image_new_from_pixbuf(pix))
        indmenuItem.get_child().set_label(("%s (%i)") % (acc.get_name(),acc.get_total_unread()))
        indmenuItem.connect('activate', self.acc_activate_cb, acc)
        indmenuItem.set_always_show_image (True)
        """
        indmenuItem = gtk.MenuItem()
        box = gtk.HBox()
        box.pack_start(gtk.image_new_from_pixbuf(pix), False, False)
        box.pack_start(gtk.Label(acc.get_name()), False, True, 10)
        total_label = gtk.Label(("(%i)") % (acc.get_total_unread()))
        box.pack_end(total_label, False, False)
        indmenuItem.add(box)
        indmenuItem.connect('activate', self.acc_activate_cb, acc)
        self.indmenu.append(indmenuItem)
        acc.indicator = indmenuItem
        acc.total_label = total_label
    
    def update_account(self, acc):
        acc.total_label.set_label(("(%i)") % (acc.get_total_unread()))

    def remove_indicator(self, acc):
        self.indmenu.remove(acc.indicator)
        acc.indicator = None
        acc.total_label = None
        
    def preferences_cb(self, widget, acc = None):
        prefs = preferences.Preferences.get_instance()
        prefs.run()
        
    def acc_activate_cb(self, widget, acc = None):
        acc.activate()
        
    def main_cb(self, widget, data = None):
        self.indmenu.show_all()
        self.indmenu.popup(None, None, gtk.status_icon_position_menu,
                           1, gtk.get_current_event_time(), self.statusIcon)
        
    def quit_cb(self, widget, data = None):
       gtk.main_quit()

    def popup_menu_cb(self, widget, button, time, data = None):
        if button == 3:
            if data:
                data.show_all()
                data.popup(None, None, gtk.status_icon_position_menu,
                           3, time, self.statusIcon)
