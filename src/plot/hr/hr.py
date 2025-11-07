import matplotlib.ticker as mticker 
import matplotlib.pyplot as plt 
import itertools 
from . import locators 
from . import spectral_types 





class HRDiagram:

    def __init__(
        self,
        hide_paths=False,
        hide_grid=True,
        hide_legend=True, 
        hide_ticks=True
    ):
        # Store feature flags
        self.hide_paths = hide_paths
        self.hide_grid = hide_grid
        self.hide_legend = hide_legend
        self.hide_ticks = hide_ticks 

        # Setup base figure and axes
        self.fig, self.ax = plt.subplots(figsize=(12.8, 7))
        self.fig.subplots_adjust(top=0.82, bottom=0.13, left=0.10, right=0.81)

        # X axis: Temperature
        self.ax.set_xlabel("Surface temperature (K)", fontsize=18, labelpad=14)
        self.ax.set_xscale("log")
        self.ax.set_xlim((80000, 1000)) 

        # Y axis: Luminosity
        self.ax.set_ylabel("Luminosity ($L_{{sun}}$)", fontsize=18, labelpad=14)
        self.ax.set_yscale("log")
        self.ax.set_ylim((1e-6, 1e8))

        # Grid, ticks, title
        self.setup_ticks() 
        self.ax.tick_params(labelsize=14, length=10, which="major")
        self.grid(alpha=0.5, which="both")
        self.ax.set_title("Evolutionary Path Across HR Diagram", fontsize=20, pad=50)

        # Setup events
        self.lines = []
        self._legend = None
        self._connect_pan_events()
        self._connect_home_events() 





    def add_path(self, history, color=None, label=None, lw=2, alpha=1, modelnum_start=None, modelnum_end=None):
        """Add an evolutionary track to the HR diagram."""
        ind_start = 0 if modelnum_start is None else modelnum_start - 1
        ind_end = -1 if modelnum_end is None else modelnum_end - 1

        line, = self.ax.plot(
            10**history.log_Teff[ind_start:ind_end],
            10**history.log_L[ind_start:ind_end],
            color=color,
            label=label,
            lw=lw,
            alpha=alpha
        )
        self.lines.append(line)





    def grid(self, **kwargs):
        """Enable grid with initial settings."""
        self.ax.grid(True, **kwargs)





    def legend(self, **kwargs):
        """Create a legend and optionally connect it to hide during panning."""
        self._legend = self.ax.legend(**kwargs)





    def setup_ticks(self): 

        # X axis 
        self.ax.xaxis.set_major_locator(locators.MajorLogLocator()) 
        self.ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}")) 
        self.ax.xaxis.set_minor_locator(locators.MinorLogLocator()) 
        self.ax.xaxis.set_minor_formatter(mticker.NullFormatter())  
        
        # Y axis 
        self.ax.yaxis.set_major_locator(mticker.LogLocator(numticks=5))
        self.ax.yaxis.set_minor_locator(mticker.LogLocator(subs='auto', numticks=2))





    def _connect_pan_events(self):
        """Central event manager for hiding features during pan and zoom."""



        def check_if_valid_event(event, check_for_inaxes): 
            """Make sure the button press is actually a pan/zoom"""
            if event.button not in (1, 3): 
                return False 
            if check_for_inaxes: 
                if event.inaxes != self.ax:
                    return False
            toolbar = getattr(event.canvas, "toolbar", None)
            if toolbar == False: 
                return False 
            if toolbar.mode not in ("pan/zoom", "zoom rect"): 
                return False 
            else: 
                return True 



        def on_press(event):

            # Escape if button press not valid 
            if check_if_valid_event(event, check_for_inaxes=True) == False: 
                return 
            
            # Hide evolutionary tracks 
            if self.hide_paths:
                for line in self.lines:
                    line.set_visible(False)

            # Hide grid during pan
            if self.hide_grid:
                self.ax.grid(False, which='major')
                self.ax.grid(False, which='minor')

            # Hide legend during pan
            if self.hide_legend and self._legend is not None:
                self._legend.set_visible(False)

            # Hide ticks labels during pan
            if self.hide_ticks:

                # X axis 
                self.ax.xaxis.set_major_locator(mticker.NullLocator()) 
                self.ax.xaxis.set_major_formatter(mticker.NullFormatter()) 
                self.ax.xaxis.set_minor_locator(mticker.NullLocator()) 
                self.ax.xaxis.set_minor_formatter(mticker.NullFormatter())  

                # Y axis 
                self.ax.yaxis.set_major_locator(mticker.NullLocator()) 
                self.ax.yaxis.set_minor_locator(mticker.NullLocator()) 
            
            # Hide spectral labels and spans
            self._set_spectral_label_visibility(False) 
            if self.hide_spectraltype_spans: 
                self._set_spectral_spans_visibility(False)
            
            self.fig.canvas.draw_idle()



        def on_release(event):

            # Escape if button press not valid 
            if check_if_valid_event(event, check_for_inaxes=False) == False: 
                return 
            
            # Restore evolutionary tracks 
            if self.hide_paths:
                for line in self.lines:
                    line.set_visible(True)

            # Restore grid
            if self.hide_grid:
                self.ax.grid(True, which='major')
                self.ax.grid(True, which='minor')

            # Restore legend
            if self.hide_legend and self._legend is not None:
                self._legend.set_visible(True)

            # Restore minor ticks
            if self.hide_ticks:
                self.setup_ticks() 

            # Restore visibility and recalculate labels
            self._draw_spectral_labels()  
            if self.hide_spectraltype_spans: 
                self._set_spectral_spans_visibility(True)
                
            self.fig.canvas.draw_idle()



        self.fig.canvas.mpl_connect('button_press_event', on_press)
        self.fig.canvas.mpl_connect('button_release_event', on_release)





    def add_spectral_type_labels(self, min_spacing_pixels=100, hide_spectraltype_spans=True):
        """
        Add spectral type labels (OBAFGKM sequence) and shaded spectral bands.
        Labels automatically hide during pan/zoom and reappear afterward.
        """

        # Store settings and initialize storage
        self.hide_spectraltype_spans = hide_spectraltype_spans
        self._min_spacing_pixels = min_spacing_pixels
        self._spectral_label_elements = []   # list of (text, line) pairs
        self._spectral_spans = []
        self._spectral_color_cycle = itertools.cycle(["black", "white"])



        # --- Helper: Determine which subtypes fit in current view ---
        def _sample_visible_subtypes():
            xmax, xmin = self.ax.get_xlim()
            selected = []
            spectral_letters = "OBAFGKM"

            for stype in spectral_types.SPECTRAL_TYPES:
                if stype.letter not in spectral_letters:
                    continue
                for subtype in stype.subtypes:
                    if xmin <= subtype.temp <= xmax:
                        x_disp = self.ax.transData.transform((subtype.temp, 0))[0]
                        if not selected or abs(x_disp - selected[-1][1]) >= min_spacing_pixels:
                            selected.append((subtype, x_disp))
            return [subtype for subtype, _ in selected]



        # --- Helper: Draw or refresh labels ---
        def _draw_labels():
            # Remove old labels
            for txt, line in getattr(self, "_spectral_label_elements", []):
                txt.remove()
                line.remove()
            self._spectral_label_elements = []

            subtypes_to_display = _sample_visible_subtypes()
            transform = self.ax.get_xaxis_transform(which='grid')

            for subtype in subtypes_to_display:
                x = subtype.temp

                # Connector line (like a tick)
                connector = self.ax.plot(
                    [x, x], [1.0, 1.015],
                    transform=transform, color='black', lw=1.0, clip_on=False
                )[0]

                # Text label
                txt = self.ax.text(
                    x, 1.02,
                    subtype.label,
                    transform=transform,
                    ha='center', va='bottom',
                    fontsize=14, color='black'
                )

                self._spectral_label_elements.append((txt, connector))

            self.fig.canvas.draw_idle()



        # --- Static shaded background spans ---
        if not hasattr(self, "_spectral_spans") or not self._spectral_spans:
            for st in spectral_types.SPECTRAL_TYPES:
                span = self.ax.axvspan(
                    st.temp_range[1], st.temp_range[0],
                    color=next(self._spectral_color_cycle), alpha=0.05
                )
                self._spectral_spans.append(span)

        # Store helper functions for later re-use
        self._draw_spectral_labels = _draw_labels
        self._sample_visible_subtypes = _sample_visible_subtypes

        # Initial draw
        _draw_labels()





    def _set_spectral_label_visibility(self, visible):
        """Show or hide both text and connector lines."""
        if not hasattr(self, "_spectral_label_elements"):
            return
        for txt, connector in self._spectral_label_elements:
            txt.set_visible(visible)
            connector.set_visible(visible)





    def _set_spectral_spans_visibility(self, visible):
        """Show or hide the background spectral spans."""
        if not hasattr(self, "_spectral_spans"):
            return
        for span in self._spectral_spans:
            span.set_visible(visible)





    def _connect_home_events(self): 

        def _refresh_spectral_labels(event=None):
            if hasattr(self, "_draw_spectral_labels"):
                self._draw_spectral_labels()
                self.fig.canvas.draw_idle()



        # Ensure the toolbar is initialized
        manager = plt.get_current_fig_manager()
        toolbar = manager.toolbar

        # For Qt-based backends, toolbar has .actions() that list all buttons
        for action in toolbar.actions(): 
            if action.text().lower() in ["home", "back", "forward"]:
                action.triggered.connect(_refresh_spectral_labels)
            
