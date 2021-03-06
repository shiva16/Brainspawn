""" Abstract base class for plots.
"""

import gtk
from abc import ABCMeta, abstractmethod
from views.canvas_item import CanvasItem
from plots.configuration import Configuration

REGISTERED_PLOTS = {}


def registered_plot(cls):
    """ Decorator for plot implementations.
    """
    REGISTERED_PLOTS[cls.__name__] = cls
    return cls


class BasePlot(CanvasItem):
    """ Base plot class.
    In order to add plots to the visualizer, you will want to
    inherit from this class.

    Note that subclasses must call the base class constructor.
    """

    __metaclass__ = ABCMeta

    def __init__(self, main_controller, nengo_obj, capability):
        super(BasePlot, self).__init__(main_controller)
        """ Plot constructor.
        Initializes default config values for all plots,
        and sets up the plot view.

        Args:
            main_controller (VisualizerController): The top-level controller
            of the visualizer.
            nengo_obj (Nengo): The nengo object this plot is visualizing.
            capability (Capability): The capability of the object that this
            graph is visualizing.
        """
        self.nengo_obj = nengo_obj
        self.capability = capability

    def _build_context_menu(self):
        """ Context menu setup.
        """
        super(BasePlot, self)._build_context_menu()
        remove_item = gtk.MenuItem("Remove")
        remove_item.connect("activate", self.remove_plot, self.canvas)

        self._context_menu.append(remove_item)

        self._context_menu.show_all()

    def init_default_config(self):
        """ Sets default config values for all plots.
        The values contained in this dictionary are used to configure
        the plot.

        For convenience in title string formatting,
        we set 'TARGET' and 'DATA' to default values of the
        target object, and represented data, respectively.
        """
        super(BasePlot, self).init_default_config()

        if not self.nengo_obj or not self.capability:
            return

        self.config['TARGET'] = Configuration(configurable=False,
                                              value=self.nengo_obj.label)
        self.config['DATA'] = Configuration(configurable=False,
                                            value=self.capability.name.title())

    @property
    def title(self):
        """ Returns a title for the current graph.
        Format the string using self.config as the format dictionary.

        Returns:
            string. A string to use as the title of the current graph.

        Note the availability of TARGET and DATA for use in the title
        format string.
        """
        try:
            config_values_dict = self.get_config_values()
            title = self.config['title'].value.format(**config_values_dict)
        except (KeyError, ValueError) as e:
            title = self.config['title'].value
        return title

    @property
    def dimensions(self):
        """ Get the dimensions of the object this graph is representing.

        Returns:
            int. The output dimensions we are plotting.
        """
        return self.capability.get_out_dimensions(self.nengo_obj)

    @staticmethod
    def plot_name():
        """ What we call the plot.
        Used when choosing plot from dropdown menu
        """
        raise NotImplementedError("Not implemented")

    @staticmethod
    def supports_cap(capability):
        """ Return true if this plot supports the given capability.

        Args:
            capability (Capability): The capability to check for.
        """
        raise NotImplementedError("Not implemented")

    @abstractmethod
    def update(self, start_step, step_size, data):
        """ Callback function passed to observer nodes.

        Args:
            start_step (int): The initial step of the given data.
            step_size (float): The time, in simulated seconds, one step
            represents.
            data (numpy.ndarray): The data from the simulator to plot.
        """
        pass

    def remove_plot(self, widget, canvas):
        self.main_controller.remove_plot_for_obj(self, self.nengo_obj,
                                                 self.capability)
