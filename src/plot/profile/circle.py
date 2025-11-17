import numpy as np 
import matplotlib.ticker as mticker 
import matplotlib.patches as mpatches 
import matplotlib.colors as mcolors 
import matplotlib.pyplot as plt 

from . import xaxis_options 





# Add a box inside the colorbar to show the range of values it reaches, while keeping the vmin and vmax of the plot the same 
def add_colorbar_range(fig, ax, pcolormesh, colorbar_label, img_min=None, img_max=None): 

    cbar_min, cbar_max = pcolormesh.get_clim() 
    if img_min is None: 
        img_min = np.min(pcolormesh.get_array()) 
    if img_max is None: 
        img_max = np.max(pcolormesh.get_array()) 

    # Location of min/max color reached in image, relative to colorbar axis 
    # 0 means the value is equal to the bottom of the colorbar axis, 1 is the top of the colorbar
    axis_min = (img_min-cbar_min)/(cbar_max-cbar_min)
    axis_max = (img_max-cbar_min)/(cbar_max-cbar_min)

    # Initialize colorbar, remove default border     
    cbar = fig.colorbar(pcolormesh, ax=ax, label=colorbar_label)
    # cbar.locator = mticker.MaxNLocator(nbins=10)  
    cbar_ax = cbar.ax
    cbar.outline.set_visible(False)

    # White gap above and below inset colorbar 
    width_gap = 0.005   
    gap_above = mpatches.Rectangle(
        (-0.25, axis_min-width_gap),  
        width=1.5,  
        height=width_gap,  
        transform=cbar_ax.transAxes,
        facecolor=fig.get_facecolor(), 
        linewidth=0,
        edgecolor="none"
    )
    cbar_ax.add_patch(gap_above)

    gap_below = mpatches.Rectangle(
        (-0.25, axis_max),  
        width=1.5,  
        height=width_gap,  
        transform=cbar_ax.transAxes,
        facecolor=fig.get_facecolor(), 
        linewidth=0,
        edgecolor="none"
    )
    cbar_ax.add_patch(gap_below)


    # Black border around inset colorbar 
    border_bottom = mpatches.Rectangle(
        (-0.25, axis_min),  
        width=1.5,  
        height=0.004,   
        transform=cbar_ax.transAxes,
        facecolor="black", 
        linewidth=0,
        edgecolor="none"
    )
    cbar_ax.add_patch(border_bottom)

    border_top = mpatches.Rectangle(
        (-0.25, axis_max),  
        width=1.5,  
        height=-0.005,   
        transform=cbar_ax.transAxes,
        facecolor="black", 
        linewidth=0,
        edgecolor="none"
    )
    cbar_ax.add_patch(border_top)

    border_left = mpatches.Rectangle(
        (0, axis_min),  
        width=0.08,  
        height=axis_max-axis_min,   
        transform=cbar_ax.transAxes,
        facecolor="black", 
        linewidth=0,
        edgecolor="none"
    )
    cbar_ax.add_patch(border_left)
 
    border_right = mpatches.Rectangle(
        (0.93, axis_min),  
        width=0.08,  
        height=axis_max-axis_min,   
        transform=cbar_ax.transAxes,
        facecolor="black", 
        linewidth=0,
        edgecolor="none"
    )
    cbar_ax.add_patch(border_right)


    # Narrow the non=focused colorbar 
    narrow_bottom_left = mpatches.Rectangle(
        (0, axis_min-width_gap),  
        width=0.1,  
        height=-1,   
        transform=cbar_ax.transAxes,
        facecolor=fig.get_facecolor(), 
        linewidth=0,
        edgecolor="none"
    )
    cbar_ax.add_patch(narrow_bottom_left)
 
    narrow_bottom_right = mpatches.Rectangle(
        (0.91, axis_min-width_gap),  
        width=0.1,  
        height=-1,   
        transform=cbar_ax.transAxes,
        facecolor=fig.get_facecolor(), 
        linewidth=0,
        edgecolor="none"
    )
    cbar_ax.add_patch(narrow_bottom_right)

    narrow_top_left = mpatches.Rectangle(
        (0, axis_max+width_gap),  
        width=0.1,  
        height=1,   
        transform=cbar_ax.transAxes,
        facecolor=fig.get_facecolor(), 
        linewidth=0,
        edgecolor="none"
    )
    cbar_ax.add_patch(narrow_top_left)
 
    narrow_top_right = mpatches.Rectangle(
        (0.91, axis_max+width_gap),  
        width=0.1,  
        height=1,   
        transform=cbar_ax.transAxes,
        facecolor=fig.get_facecolor(), 
        linewidth=0,
        edgecolor="none"
    )
    cbar_ax.add_patch(narrow_top_right)
    return cbar 





def make_smooth_cmap(base_color, name='smooth_colormap', N=256, dark_factor=0.4, mid_pos=0.6):
    """
    Create a smoother white->base->dark colormap with controllable spacing.

    Parameters:
        base_color : str or tuple
            Matplotlib color (e.g., 'tab:blue', '#1f77b4')
        name : str
            Name for the colormap
        N : int
            Number of levels in the colormap
        dark_factor : float
            Factor (0-1) to darken the base color
        mid_pos : float
            Position of the base color in [0,1]; smaller = more light range
    """
    base_rgb = np.array(mcolors.to_rgb(base_color))
    dark_rgb = base_rgb * dark_factor  # darker version of base color

    # Define (position, color) pairs
    colors = [
        (0.0, (1, 1, 1)),     # start (white)
        (mid_pos, base_rgb),  # where base color appears
        (1.0, dark_rgb)       # end (dark)
    ]
    
    return mcolors.LinearSegmentedColormap.from_list(name, colors, N=N)





def circle_plot(ax, profile, f_r, xaxis=xaxis_options.PROFILEXAXIS_RADIUS, cmap=None, color=None, vmin=None, vmax=None, title=None, colorbar_label=None, r_max=None):
    """
    Plot a circular radial intensity pattern using a polar projection.
    
    Parameters:
        r               : array-like, radial coordinates (either mass coordinate or radius) 
        f_r             : array-like, intensity values corresponding to r (i.e., f(r))
        cmap            : str, colormap name
        vmin, vmax      : color normalization limits (optional)
    """

    r = xaxis.get_values(profile)
    r_units_str = xaxis.xlabel_units

    # Make sure only one of either COLOR or COLORMAP are provided (not both)
    if cmap is None and color is None: 
        raise ValueError 
    if cmap is not None and color is not None: 
        raise ValueError 
    if cmap is None and color is not None:  
        cmap = make_smooth_cmap(color) 
    if cmap is not None and color is None: 
        pass 

    # Add extra points near zero so it doesn't look like there's a hole at the center of the star 
    for _ in range(100): 
        f_r = np.append(f_r, f_r[np.argmin(r)])
        r = np.append(r, np.min(r)/2) 

    # Polar plot 
    theta = np.linspace(0, 2 * np.pi, 360)
    R, THETA = np.meshgrid(r, theta)
    H = np.tile(f_r, (len(theta), 1))
    mesh = ax.pcolormesh(THETA, R, H, cmap=cmap, shading='auto', vmin=vmin, vmax=vmax)

    # Title and y label 
    # ax.set_title(title, fontsize=20, pad=15)
    # ax.set_xlabel(f"Location inside star {r_units_str}", fontsize=14)

    # R limit 
    if r_max is not None: 
        ax.set_ylim(0, r_max)

    # Grid 
    # ax.grid(color="black", lw=0.5, alpha=0.5)

    # # X ticks (vertical line)
    # ax.set_xticks([270*np.pi/180])
    # ax.set_xticklabels([]) 

    # # Y ticks 
    # ax.set_rlabel_position(270)  # move labels to a clean spot (in degrees)
    # ax.yaxis.set_major_locator(mticker.MaxNLocator(nbins=4))
    # ax.set_yticklabels(["" if tick == 0 else f"{tick}" for tick in ax.get_yticks()])

    ax.set_xticks([])
    ax.set_yticks([])


    # # Remove border around axis and set figure backbround to light gray, in order to better distinguish the edge of the star 
    # fig.set_facecolor((0.95, 0.95, 0.95))
    # for spine in ax.spines.values():
    #     spine.set_linewidth(0.0) 
    
    # # Color bar 
    # if r_max is not None: 
    #     ind_within_plot = np.where(r<=r_max) 
    #     img_min = np.nanmin(f_r[ind_within_plot]) 
    #     img_max = np.nanmax(f_r[ind_within_plot]) 
    # else: 
    #     img_min = None 
    #     img_max = None 
    # cbar = add_colorbar_range(fig, ax, mesh, colorbar_label, img_min=img_min, img_max=img_max)
    # cbar.ax.tick_params(labelsize=12, length=4)    # tick numbers and tick size
    # cbar.set_label(colorbar_label, fontsize=14, labelpad=14)  # label size and spacing

    return mesh
