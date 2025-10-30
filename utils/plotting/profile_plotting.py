import numpy as np 
from dataclasses import dataclass 

import matplotlib.pyplot as plt 
import matplotlib.ticker as mticker 
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties

import utils.config.physical_constants as physical_constants 
import utils.config.plot_options as plot_options 
import utils.config.profile_xaxis_options as profile_xaxis_options




# Dataclass that holds plot parameters that need to be passed to ProfilePlot._setup() when initializing a plot 
@dataclass
class ProfilePlotConfigParams:
    ylabel: str
    ylim: tuple | None
    yscale: str
    title: str





# Class that holds all profile plots so that the shared code can be held in a setup() function 
# Example usage: 
# import utils.plotting.profile_plotting as profile_plotting 
# fig = profile_plotting.ProfilePlot.convection(profile, ui_options.PROFILEXAXIS_MASS) 
# fig = profile_plotting.ProfilePlot.composition(profile, ui_options.PROFILEXAXIS_MASS, history) 
class ProfilePlot:



    # Code shared by all profile plots 
    @staticmethod
    def _setup(profile, xaxis, config): 

        # Create figure 
        fig, ax = plt.subplots(figsize=(12.5, 5))
        fig.subplots_adjust(top=0.86, bottom=0.16, left=0.10, right=0.81)

        # Select either mass or radius as the x axis 
        x_arr = xaxis.get_values(profile)
        x_units_str = xaxis.xlabel_units

        # Set xlabel (mass or radius) and xlim  
        ax.set_xlabel(f"Location inside star {x_units_str}", fontsize=18)
        ax.set_xlim(0, 1.001*np.max(x_arr))


        # Add text labels to left side ("Center") and right side ("Surface") of x axis  
        ax.text(
            0, -0.11,       
            "(Center)",
            transform=ax.get_xaxis_transform(),  
            ha="center", va="top", fontsize=12, 
        )

        ax.text(
            np.max(x_arr), -0.11,       
            "(Surface)",
            transform=ax.get_xaxis_transform(),  
            ha="center", va="top", fontsize=12, 
        )
        
        # Set ylabel and yscale  
        ax.set_ylabel(config.ylabel, fontsize=18, labelpad=14) 
        ax.set_yscale(config.yscale) 

        # Set ylim 
        # If ylim is None, do nothing because setting the ylims is handled by the individual plotting function 
        # Useful when ylims need to be calculated rather than being a known constant value 
        if config.ylim is not None: 
            ax.set_ylim(config.ylim[0], config.ylim[1]) 

        # Set title and subtitle 
        ax.set_title(config.title, fontsize=20, pad=25) 
        ax.text(
            0.5, 1.025, 
            f"{profile.initial_mass_string} $M_{{sun}}$ star at {profile.age_string} years old (model number={profile.modelnum})", 
            transform=ax.transAxes, 
            fontsize=12, ha='center')

        # Grid, ticks 
        ax.grid(alpha=0.5) 
        ax.tick_params(labelsize=14) 

        return fig, ax 
    


    # Profile plot: composition vs mass/radius
    @classmethod
    def composition(cls, profile, xaxis=profile_xaxis_options.PROFILEXAXIS_MASS, history=None): 

        # Most plots don't require a history, but this one does. If the user forgets to provide it, raise an error. 
        if history is None: 
            raise ValueError("Composition plot requires 'history' to be provided")

        # Setup 
        config = ProfilePlotConfigParams(
            ylabel="Composition (mass fraction)",
            ylim=(-0.01, 1.01),
            yscale="linear",
            title="Interior composition")
        fig, ax = cls._setup(profile, xaxis, config)
        x_arr = xaxis.get_values(profile)
        
        # Sort elements by maximum value so it plots the most important ones first (puts them on the top of the legend)
        isotope_values = [
            (isotope, np.nanmax(getattr(profile, isotope.profile_key)))
            for isotope in plot_options.ISOTOPES
        ]
        isotope_values.sort(key=lambda x: x[1], reverse=True)

        # Loop through list of Isotope objects 
        for z_index, (isotope, max_val) in enumerate(isotope_values):
            if max_val > 0:
                composition_profile = getattr(profile, isotope.profile_key)
                ax.plot(
                    x_arr,
                    composition_profile,
                    label=isotope.label,
                    color=isotope.color,
                    lw=3,
                    zorder=len(isotope_values) - z_index  # highest value = plotted last (on top)
                )

            # Add horizontal dashed lines showing the initial composition
            if isotope.show_initial_abundance: 
                composition_history = getattr(history, isotope.history_key)
                ax.axhline(composition_history[0], color=isotope.color, ls="dashed") 

        # Legend 
        ax.legend(fontsize=12, loc="center left", bbox_to_anchor=(1, 0.5)) 

        return fig 
    


    # Profile plot: composition vs mass/radius
    @classmethod
    def composition_log(cls, profile, xaxis=profile_xaxis_options.PROFILEXAXIS_MASS, history=None): 

        # Most plots don't require a history, but this one does. If the user forgets to provide it, raise an error. 
        if history is None: 
            raise ValueError("Composition plot requires 'history' to be provided")

        # Setup 
        ymin = 1e-9
        config = ProfilePlotConfigParams(
            ylabel="Composition (mass fraction)",
            ylim=(ymin, 1),
            yscale="log",
            title="Interior composition")
        fig, ax = cls._setup(profile, xaxis, config)
        x_arr = xaxis.get_values(profile)
        
        # Sort elements by maximum value so it plots the most important ones first 
        isotope_values = [
            (isotope, np.nanmax(getattr(profile, isotope.profile_key)))
            for isotope in plot_options.ISOTOPES
        ]
        isotope_values.sort(key=lambda x: x[1], reverse=True)

        # Loop through list of Isotope objects 
        for isotope, max_val in isotope_values: 

            # Only plot profiles that are significant
            if max_val > 0: 
                composition_profile = getattr(profile, isotope.profile_key)
                ax.plot(
                    x_arr,
                    composition_profile,
                    label=isotope.label,
                    color=isotope.color,
                    lw=3
                ) 

            # Add horizontal dashed lines showing the initial composition
            composition_history = getattr(history, isotope.history_key)
            ax.axhline(composition_history[0], color=isotope.color, ls="dashed") 

        # Legend 
        ax.legend(fontsize=12, loc="center left", bbox_to_anchor=(1, 0.5)) 

        return fig 



    # Profile plot: Convection vs mass/radius 
    @classmethod 
    def convection(cls, profile, xaxis=profile_xaxis_options.PROFILEXAXIS_MASS, history=None): 

        # Setup 
        config = ProfilePlotConfigParams(
            ylabel="Strength of convection",
            ylim=(1e0, 1e20),
            yscale="log",
            title="Heat transport regions inside star")
        fig, ax = cls._setup(profile, xaxis, config)
        x_arr = xaxis.get_values(profile)
        
        # Convection plots 
        ax.plot(x_arr, 10**profile.log_D_conv, label="Convective", lw=3) 
        ax.plot(x_arr, 10**profile.log_D_semi, label="Semiconvective", lw=3) 
        ax.plot(x_arr, 10**profile.log_D_ovr, label="Overshoot", lw=3) 
        ax.plot(x_arr, 10**profile.log_D_thrm, label="Thermohaline", lw=3) 

        # Legend 
        ax.legend(fontsize=12, loc="center left", bbox_to_anchor=(1, 0.5)) 

        return fig 



    # Profile plot: fusion rate vs mass/radius 
    @classmethod 
    def fusion(cls, profile, xaxis=profile_xaxis_options.PROFILEXAXIS_MASS, history=None): 

        # Setup 
        config = ProfilePlotConfigParams(
            ylabel="Fusion rate (ergs/sec/gram)",
            ylim=None,
            yscale="log",
            title="Interior fusion rate")
        fig, ax = cls._setup(profile, xaxis, config)
        x_arr = xaxis.get_values(profile)
        
        # Plot fusion rates 
        ax.plot(x_arr, profile.eps_nuc, label = "Total fusion", lw=2, color="black")
        ax.plot(x_arr, profile.pp, label = "Hydrogen \u2192 Helium \n(PP chain)", lw=3, color="#00759C")
        ax.plot(x_arr, profile.cno, label = "Hydrogen \u2192 Helium \n(CNO cycle)", lw=3, color="#71D2FF")
        ax.plot(x_arr, profile.tri_alfa, label = "Helium \u2192 Carbon \n(triple alpha)", lw=3, color="tab:green")
        metal_fusion = profile.eps_nuc - profile.pp - profile.cno - profile.tri_alfa 
        ax.plot(x_arr, metal_fusion, label="Heavier elements", lw=3, color="tab:red") 
        
        # Set ylim 
        # Calculate the average ergs/sec/gram of the entire star's mass and luminosity 
        specific_L = np.max(profile.luminosity)*physical_constants.L_sun / (profile.initial_mass*physical_constants.M_sun) 
        max_fusion = np.max(profile.eps_nuc) 
        if max_fusion>specific_L: 
            ax.set_ylim((specific_L/10, max_fusion)) 
        else: 
            ax.set_ylim((specific_L/10, specific_L*1000))

        # Legend 
        ax.legend(fontsize=12, loc="center left", bbox_to_anchor=(1, 0.5)) 

        return fig 
    
    

    # Profile plot: mu (mass/particule) vs mass/radius 
    @classmethod 
    def mu(cls, profile, xaxis=profile_xaxis_options.PROFILEXAXIS_MASS, history=None): 

        # Setup 
        config = ProfilePlotConfigParams(
            ylabel="Mass/particle (AMU)",
            ylim=None,
            yscale="linear",
            title=f"Interior $\mu$ profile")
        fig, ax = cls._setup(profile, xaxis, config)
        x_arr = xaxis.get_values(profile)
        
        # Plot mass/particle
        ax.plot(x_arr, profile.mu, color="gray", lw=2, label=f"Current $\mu$") 
            
        # Horizontal lines at 1.34 and 0.6 to represent mu of pure helium and mu of envelope 
        ax.axhline(0.62, color="black", linestyle="dashed", label=f"Initial $\mu$")
        ax.axhline(4/3, color="tab:green", linestyle="dashed", label="Pure helium \n(theoretical)")
        ax.axhspan(12/7, 16/9, color="#c0450852", label="C+O mixture \n(theoretical)") 

        # Set ylim 
        xmax = 0.95*np.max(x_arr) 
        ind_within_xlim = np.where(x_arr<xmax)
        mu_max = np.nanmax(profile.mu[ind_within_xlim]) 
        y_max = 1.44 
        if mu_max > 1.39: 
            y_max = 1.9 
        ax.set_ylim((0.5, y_max))

        # Legend 
        ax.legend(fontsize=12, loc="center left", bbox_to_anchor=(1, 0.5)) 

        return fig 
    


    # Profile plot: temperature vs mass/radius 
    @classmethod 
    def temp(cls, profile, xaxis=profile_xaxis_options.PROFILEXAXIS_MASS, history=None): 

        # Setup 
        config = ProfilePlotConfigParams(
            ylabel="Temperature (K)",
            ylim=None,
            yscale="linear",
            title="Interior temperature profile")
        fig, ax = cls._setup(profile, xaxis, config)
        x_arr = xaxis.get_values(profile)


        # # Number densities 
        # n_baryon = 10**profile.logRho / physical_constants.m_p 
        # n_free_e = n_baryon * profile.free_e 
        # n_total = n_baryon / profile.mu 
        # n_ion = n_total - n_free_e

        # # Kinetic energy per particle 
        # KE_electron = 3/2 * profile.pressure / n_free_e 
        # KE_baryon = 3/2 * profile.pressure / n_baryon 

        # ax.plot(x_arr, KE_electron, lw=3, label="Electrons")
        # ax.plot(x_arr, KE_baryon, lw=3, label="Baryons")


        # Calculate kinetic energy per particle from the temperature (assuming ideal gas) + what it actually is 
        KE_per_N_temp = 10**profile.logT 
        KE_per_N_actual = profile.pressure * profile.mu*physical_constants.m_p / (10**profile.logRho) / physical_constants.k
        ax.plot(x_arr, KE_per_N_temp, lw=3, label="Temperature (K)") 
        ax.plot(x_arr, KE_per_N_actual, lw=3, label="KE/particle") 
      
        # Set y limit to focus on the core 
        xmax = 0.95*np.max(x_arr) 
        ind_within_xlim = np.where(x_arr<xmax)
        ymin1 = np.min(KE_per_N_temp[ind_within_xlim]) 
        ymin2 = np.min(KE_per_N_actual[ind_within_xlim]) 
        ymin = np.min([ymin1, ymin2]) 
        ymax1 = np.max(KE_per_N_temp[ind_within_xlim]) 
        ymax2 = np.max(KE_per_N_actual[ind_within_xlim]) 
        ymax = np.max([ymax1, ymax2])
        ax.set_ylim(0, ymax) 

        ax.yaxis.set_major_formatter(mticker.EngFormatter()) 

        # Legend 
        ax.legend(fontsize=12, loc="center left", bbox_to_anchor=(1, 0.5)) 

        return fig 
    


    # Profile plot: temperature gradient (radiative vs convective) vs mass/radius 
    @classmethod 
    def tempgrad(cls, profile, xaxis=profile_xaxis_options.PROFILEXAXIS_MASS, history=None): 

        # Setup 
        config = ProfilePlotConfigParams(
            ylabel="Temperature gradient",
            ylim=None,
            yscale="linear", 
            title="Interior temperature gradient")
        fig, ax = cls._setup(profile, xaxis, config)
        x_arr = xaxis.get_values(profile)

        # 3 temperature gradients: Actual/observed, plus theoretical radiative and adiabatic for comparison 
        ax.plot(x_arr, profile.gradT, lw=5, color="black", label="Actual") 
        ax.plot(x_arr, profile.grada, lw=2, color="red", label="Adiabatic \n(theoretical)")
        ax.plot(x_arr, profile.gradr, lw=2, color="limegreen", label="Radiative \n(theoretical)")

        # Set ylim         
        old_ymin = min(profile.gradT) 
        old_ymax = max(profile.gradT) 
        diff = old_ymax-old_ymin
        amplitude = diff/2
        center = old_ymin+amplitude
        padding_fraction = 1.2 # Extra room above and below the old ylims 
        new_ymin = center - amplitude*padding_fraction 
        new_ymax = center + amplitude*padding_fraction 
        ax.set_ylim(new_ymin, new_ymax)

        # Legend 
        ax.legend(fontsize=12, loc="center left", bbox_to_anchor=(1, 0.5)) 

        return fig 



    # Profile plot: How close to degeneracy are the electrons and the baryons 
    @classmethod 
    def degeneracy(cls, profile, xaxis=profile_xaxis_options.PROFILEXAXIS_MASS, history=None): 

        # Setup 
        config = ProfilePlotConfigParams( 
            ylabel="Relative spacing  ($n^{-1/3}$ / $\lambda_{dB}$)", 
            ylim=(1e-2, 1e4), 
            yscale="log", 
            title="Degeneracy of electrons and baryons"
        )
        fig, ax = cls._setup(profile, xaxis, config) 
        x_arr = xaxis.get_values(profile) 

        # Use shading to represent transition from ideal to degenerate 
        ax.axhspan(ymin=1, ymax=1e10, color="green", alpha=0.07, label="Particles \nfar apart \n(Ideal)") 
        ax.axhspan(ymin=1e-8, ymax=1, color="red", alpha=0.07, label="Particles \noverlapping \n(Degen)")

        # Number densities 
        n_baryon = 10**profile.logRho / physical_constants.m_p 
        n_free_e = n_baryon * profile.free_e 
        n_total = n_baryon / profile.mu 
        n_ion = n_total - n_free_e

        # Average interparticle spacing 
        interparticle_spacing_free_e = n_free_e**(-1/3) 
        interparticle_spacing_baryon = n_baryon**(-1/3) 

        # Kinetic energy per particle 
        KE_electron = 3/2 * profile.pressure / n_free_e 
        KE_baryon = 3/2 * profile.pressure / n_baryon 

        # Momentum per particle 
        p_electron = np.sqrt( (KE_electron / physical_constants.c)**2 + 2*KE_electron*physical_constants.m_e )
        p_baryon = np.sqrt( (KE_baryon / physical_constants.c)**2 + 2*KE_baryon*physical_constants.m_p )

        # De broglie wavelength 
        deBroglie_wavelength_electron = physical_constants.h / p_electron 
        deBroglie_wavelength_baryon = physical_constants.h / p_baryon

        # Plot degeneracy 
        electron_color = "tab:blue" 
        baryon_color = "tab:orange"
        ax.plot(x_arr, interparticle_spacing_free_e / deBroglie_wavelength_electron, lw=3, label="Electrons", color=electron_color) 
        ax.plot(x_arr, interparticle_spacing_baryon / deBroglie_wavelength_baryon, lw=3, label="Baryons", color=baryon_color) 

        # Find where sign changes (crosses the threshold) 
        threshold = 1 
        for (y, color) in [(interparticle_spacing_free_e / deBroglie_wavelength_electron, electron_color), (interparticle_spacing_baryon / deBroglie_wavelength_baryon, baryon_color)]: 
            crossings = np.where(np.diff(np.sign(y - threshold)) != 0)[0]
            for crossing in crossings: 
                plt.axvline(x_arr[crossing], color=color, ls="dotted") 
        
        # Add line separating degenerate from nondegenerate 
        ax.axhline(1, color="black") 

        # Legend 
        ax.legend(fontsize=12, loc="center left", bbox_to_anchor=(1, 0.5)) 

        return fig 






def add_colored_title(fig, strings, colors, fontsize, y=0.95, spacing_pts=10):

    ax = fig.axes[0]  
    ax.set_title("") 
    fontprops = FontProperties(family='DejaVu Sans', size=fontsize)

    def get_text_width(text, fontprops):
        tp = TextPath((0, 0), text, prop=fontprops)
        return tp.get_extents().width
    
    tp_widths = [get_text_width(p, fontprops) for p in strings]
    total_width_pts = sum(tp_widths) + spacing_pts * (len(strings) - 1)

    fig_width_in = fig.get_figwidth()
    pts_to_fig_frac = 1 / (fig_width_in * 72)

    x = 0.5 - total_width_pts * pts_to_fig_frac / 2
    for part, color, width in zip(strings, colors, tp_widths):
        fig.text(
            x, y, part, 
            fontproperties=fontprops,
            color=color, 
            ha='left', 
            va='center', 
            bbox=dict(facecolor='white', edgecolor='none', pad=5) )
        x += width * pts_to_fig_frac + spacing_pts * pts_to_fig_frac






