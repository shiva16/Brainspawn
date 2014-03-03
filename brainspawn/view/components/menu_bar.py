'''
Created on Jul 18, 2013

@author: vagrant
'''
import gtk

class Menu_Bar(gtk.MenuBar):
    '''
    classdocs
    '''


    def __init__(self, main_frame, controller):
        self.controller = controller
        '''
        Constructor
        '''
        super(Menu_Bar, self).__init__()
        file_menu = gtk.MenuItem("File")
        file_submenu = gtk.Menu()
        file_menu.set_submenu(file_submenu)

        # TODO, shoot, we need a base class for all exportable views
        export_pdf_menu_item = gtk.MenuItem("Export to PDF")
        export_pdf_menu_item.connect('activate', controller.on_export_pdf)
        export_pdf_menu_item.show()
        file_submenu.append(export_pdf_menu_item)

        file_menu.show()

        tools_menu = gtk.MenuItem("Tools")
        tools_submenu = gtk.Menu()
        tools_menu.set_submenu(tools_submenu)

        resize_menu_item = gtk.CheckMenuItem("Resize")
        resize_menu_item.connect("activate", main_frame.toggle_resize)
        tools_submenu.append(resize_menu_item)

        input_panel_menu_item = gtk.CheckMenuItem("Input Panel")
        input_panel_menu_item.connect("activate", main_frame.toggle_panel, main_frame.input_panel)
        input_panel_menu_item.show()
        tools_submenu.append(input_panel_menu_item)

        tools_menu.show()

        view_menu = gtk.MenuItem("View")
        view_submenu = gtk.Menu()
        view_menu.set_submenu(view_submenu)


        # TODO - this will go away
        #self.spectrogram_menu_item = gtk.CheckMenuItem("Spectrogram")
#        self.spectrogram_menu_item.connect("activate", main_frame.toggle_plot, main_frame.spec_canvas)
        #self.spectrogram_menu_item.show()
        #view_submenu.append(self.spectrogram_menu_item)

        for plot in main_frame.all_plots:
            menu_item = gtk.CheckMenuItem(plot.display_name())
            #menu_item.connect("activate", main_frame.show_plot, plot.canvas)
            menu_item.show()
            view_submenu.append(menu_item)

        '''
        self.xy_plot_menu_item = gtk.CheckMenuItem("XY plot")
        self.xy_plot_menu_item.connect("activate", main_frame.toggle_plot, main_frame.xy_plot.canvas)
        self.xy_plot_menu_item.show()
        view_submenu.append(self.xy_plot_menu_item)

        voltage_grid_menu_item = gtk.CheckMenuItem("Voltage Grid")
#        voltage_grid_menu_item.connect("activate", main_frame.toggle_plot, main_frame.vg_canvas)
        voltage_grid_menu_item.show()
        view_submenu.append(voltage_grid_menu_item)

        network_view_menu_item = gtk.CheckMenuItem("Network View")
#        network_view_menu_item.connect("activate", main_frame.toggle_plot, main_frame.network_canvas)
        network_view_menu_item.show()
        view_submenu.append(network_view_menu_item)

        '''

        view_menu.show()

        help_menu = gtk.MenuItem("Help")
        help_menu.show()

        self.append (file_menu)
        self.append (tools_menu)
        self.append (view_menu)
        self.append (help_menu)
