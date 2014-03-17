import gtk
from gi.repository import Gtk

class CustomizeWindow:
    def __init__(self, plot, **kwargs):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.plot = plot
        name = "Customize " + kwargs.get('name') if 'name' in kwargs else "Customize"
        self.window.set_title(name)
        
        self.options = plot.get_options_dict()
        
        self.vbox = gtk.VBox()
        self.controls = {}
        control = None
        
        for option_name in self.options:
            if (self.options[option_name].configurable):
                data_type = self.options[option_name].data_type
                text_label = gtk.Label(self.options[option_name].display_name)
                type_label = gtk.Label(data_type)
                
                if (data_type == 'text'):
                    control = gtk.Entry()
                    control.set_text(self.options[option_name].value)
                elif (data_type == 'combo'):
                    control = Gtk.ComboBoxText.new_with_entry()
                    combo_values = self.options[option_name].combo
                    for combo_value in combo_values:
                        control.append(combo_value, combo_value)
                    control.set_entry_text_column(0)
                    
                    control.set_active(combo_values.index(self.options[option_name].value))
                elif (data_type == 'boolean'):
                    control = Gtk.CheckButton()
                    control.set_active(self.options[option_name].value)
                elif (data_type == 'color'):
                    control = Gtk.Button("Color chooser...")
                    
                    color_selection_dialog = Gtk.ColorSelectionDialog()
                    control.connect("clicked", self.show_color_selection_dialog, color_selection_dialog)
                    color_selection = color_selection_dialog.get_color_selection()
                    self.controls[option_name] = color_selection
                    color_selection.connect("color_changed", self.apply_all)
                            
                if (control):
                    if (data_type == 'text' or data_type == 'combo'):
                        control.connect("changed", self.apply_all)
                    elif (data_type == 'boolean'):
                        control.connect("toggled", self.apply_all)
                        
                    if (data_type != 'color'):
                        self.controls[option_name] = control
                    
                    hbox = Gtk.HBox(True, 10)
                    hbox.pack_start(text_label, True, True, 10)
                    hbox.pack_start(type_label, True, True, 10)
                    hbox.pack_start(control, True, True, 10)
                    
                    self.vbox.pack_start(hbox, True, False, 10)

        apply_button = gtk.Button(label="Apply")
        apply_button.connect("clicked", self.apply_all)
        self.vbox.pack_start(apply_button)
        self.window.add(self.vbox)
        self.window.show_all()
        
    def show_color_selection_dialog(self, widget, dialog):
        response = dialog.run()
        if (response != Gtk.ResponseType.OK):
            color_selection = dialog.get_color_selection()
            color_selection.set_current_color(color_selection.get_previous_color())
        dialog.hide()
    
    def apply_all(self, widget):
        for option_name in self.options:
            if (self.options[option_name].function):
                function = self.options[option_name].function
                function(self.get_val(option_name))
        
        self.plot.canvas.queue_draw()
            
    def get_val(self, option_name):
        data_type = self.options[option_name].data_type
        if (data_type == 'text'):
            unformatted_string = self.controls[option_name].get_text()
            config_values = self.plot.get_config_values()
            try:
                formatted_string = unformatted_string.format(**config_values)
                return formatted_string
            except (KeyError, ValueError) as e:
                return unformatted_string
        elif (data_type == 'combo'):
            text = self.controls[option_name].get_active_text()
            self.controls[option_name].queue_draw()
            return text
        elif (data_type == 'boolean'):
            return self.controls[option_name].get_active()
        elif (data_type == 'color'):
            rgba = self.controls[option_name].get_current_color()
            return (rgba.red/65535.0, rgba.green/65535.0, rgba.blue/65535.0)
        