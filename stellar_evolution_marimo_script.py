import marimo

__generated_with = "0.13.15"
app = marimo.App(width="full")


@app.cell
def _():
    # To do: 



    # If the mass of the progenitor is between 7 and 9 solar masses (M☉), the core temperature will be sufficient to fuse carbon but not neon, in which case an oxygen–neon–magnesium (ONeMg or ONe) white dwarf may form. (https://en.wikipedia.org/wiki/White_dwarf)


    # Add progress bar 


    # Flowchart: 
    # Add "we are are" showing currently selected mass and model number 
    # Add transparent/gray boxes where the star doesn't achieve those stages with explanation why it skips those stages. I.e.: "never gets hot enough to fuse helium" 

    # HR DIAGRAM: 
    # Add transparent tracks of available but un-selected substages for comparison 

    # History plots: 
    # "We are here" vertical line showing selected model number 
    # Add an option for history plot to be either scaled linearly with time or to evenly space the substages, to make it easier to see the interesting properties that happen all near the end of the star's life
    # How to deal with helium ignition: give an option called is_instantaneous=True which overrides the need for a model_start and model_end. Instead, it uses the model_example and plots a LINE at that point rather than an axhspan, and the even spacing ignores it. 


    # Make marimo notebook available on github: 
    # Take URL to this notebook on github, which is: 
    # https://github.com/johnmomberg/Gayley_Stellar_Evolution_Textbook/blob/main/stellar_evolution_marimo_script.py 
    # Replace the https://github.com/ part with https://marimo.app/github.com/ , which gives: 
    # https://marimo.app/github.com/johnmomberg/Gayley_Stellar_Evolution_Textbook/blob/main/stellar_evolution_marimo_script.py 


    # Fix ylims of fusion vs time plot 
    # Bring ylim-setting code into its own function: one for log plots and one for linear plots 

    # Plots to make work: 
    # Comparison of de broglie wavelength to interparticle spacing 
    # Plot ionization fraction as function of interior of star 
    # Plot different species opacities (metals, electrons, hydrogen, etc)


    # I don't like the way I'm currently finding the available substages. The dictionary key which is currently calculated like set_textcolor_css(sub.mode2_abbrev_with_massrange, sub.flowchart_color) should be an attribute of the substage class. for example, i have mode1_abbrev. i should have mode1_key which would replace mode1_abbrev_with_massrange and do whatever i need to to, such as appending the mass range. 



    return


@app.cell(hide_code=True)
def _(mo):
    # Create title string "full_title"

    with mo.status.spinner(title="Creating title text...") as _: 
        full_title = mo.md("<h1>Stellar Evolution Interactive Tool</h1>") 

    return (full_title,)


@app.cell(hide_code=True)
def _(mo):
    # User Guide section header "userguide_subtitle" with switch to minimize it "userguide_switch"
    with mo.status.spinner(title="Creating User Guide section...") as _: 
        userguide_subtitle = mo.md("<h2>Tutorial/Documentation</h2>") 
        userguide_switch = mo.ui.switch(value=True, label="Hide / show")
        userguide_subtitle_hstack = mo.hstack([userguide_subtitle, userguide_switch], justify="space-between", align="center")

    return userguide_subtitle_hstack, userguide_switch


@app.cell(hide_code=True)
def _(mo, userguide_switch):
    # User guide text (shows up if user guide is not minimized) "userguide_text"

    with mo.status.spinner(title="Setting User Guide section text...") as _: 
        userguide_text = "Tutorial minimized by user" 
        if userguide_switch.value == True: 
            userguide_text = "To do: create user guide/tutorial/documentation for this app. "


    return (userguide_text,)


@app.cell(hide_code=True)
def _(mo):
    # Flowchart header "flowchart_subtitle" with switch to minimize it "flowchart_switch"
    with mo.status.spinner(title="Creating flowchart section...") as _: 
        flowchart_subtitle = mo.md("<h2>Flowchart</h2>") 
        flowchart_switch = mo.ui.switch(value=True, label="Hide / show") 
        flowchart_yaxis_dropdown = mo.ui.dropdown(options={"mass": 0, "spectral type (on MS)": 1}, value="mass", label="Flowchart y-axis shows...")
        flowchart_subtitle_hstack = mo.hstack([flowchart_subtitle, flowchart_yaxis_dropdown, flowchart_switch], justify="space-between", align="center")


    return (
        flowchart_subtitle_hstack,
        flowchart_switch,
        flowchart_yaxis_dropdown,
    )


@app.cell(hide_code=True)
def _(mo):
    # Controls section header ("controls_subtitle") and secondary plot section header ("secondary_plot_subtitle")
    with mo.status.spinner(title="Creating Controls section subheaders...") as _: 
        controls_subtitle = mo.md("<h2>Controls</h2>") 
        secondary_plot_subtitle = mo.md("<h2>Secondary Plot</h2>") 

    return controls_subtitle, secondary_plot_subtitle


@app.cell(hide_code=True)
def _(mo, ui_options):
    # Comparison mode radio 
    with mo.status.spinner(title="Creating Comparison Mode selector and subheader...") as _: 
        comparison_mode_title = mo.md("<h3>Choose mass/evolutionary stage highlighted by secondary plot</h3>") 
        comparison_mode_radio = ui_options.create_radio(ui_options.COMPAREMODE_OPTIONS) 

    return comparison_mode_radio, comparison_mode_title


@app.cell(hide_code=True)
def _(mo, stellar_evolution_data):
    # Dropdowns used by "comparison_mode_str": either "mode1_massrange_dropdown" or "mode2_parentstage_dropdown" 

    with mo.status.spinner(title="Creating comparison mode dropdowns...") as _: 


        # Mode1 
        unique_masses = sorted({m for s in stellar_evolution_data.SUBSTAGES_LIST for m in [s.mass_min, s.mass_max]})
        mode1_massrange_options = [f"{unique_masses[i]:.1f}-{unique_masses[i+1]:.1f}" for i in range(len(unique_masses)-1)]
        mode1_massrange_dropdown = mo.ui.dropdown(mode1_massrange_options, value=next(iter(mode1_massrange_options)))

        # Mode2 
        mode2_parentstage_options = {stage.full_name: stage for stage in stellar_evolution_data.ParentStage}
        mode2_parentstage_dropdown = mo.ui.dropdown(options=mode2_parentstage_options, value=next(iter(mode2_parentstage_options))) 

    return mode1_massrange_dropdown, mode2_parentstage_dropdown, unique_masses


@app.cell(hide_code=True)
def _(mo, mode1_massrange_dropdown, mode2_parentstage_dropdown):
    # Strings that go next to "comparison_mode_radio" containing dropdowns 

    with mo.status.spinner(title="Creating Comparison Mode radio options...") as _: 

        noselection_str = mo.md(f"No selection: View entire flowchart")
        massfirst_str = mo.md(f"Select mass first: View the evolution of a {mode1_massrange_dropdown} mass star")
        stagefirst_str = mo.md(f"Select stage first: Compare how stars of different masses experience the {mode2_parentstage_dropdown} stage") 
        freeselection_str = mo.md(f"Select a specific MESA file to load") 

    return freeselection_str, massfirst_str, noselection_str, stagefirst_str


@app.cell(hide_code=True)
def _(mo, ui_options):
    # Plot mode section header ("plot_mode_title") and radio selector ("plot_mode_radio")  
    with mo.status.spinner(title="Creating Plot Mode selector and subheader...") as _: 
        plot_mode_title = mo.md("<h3>Choose secondary plot</h3>") 
        plot_mode_radio = ui_options.create_radio(ui_options.PLOTMODE_OPTIONS)

    return plot_mode_radio, plot_mode_title


@app.cell(hide_code=True)
def _(mo):
    # Plot mode HR diagram string "HR_diagram_str"
    with mo.status.spinner(title="Creating HR Diagram plot mode text...") as _: 
        HR_diagram_str = mo.md("HR diagram")

    return (HR_diagram_str,)


@app.cell(hide_code=True)
def _(mo, ui_options):
    # Plot mode history string "history_str" which contains the dropdown "history_plot_dropdown" 
    with mo.status.spinner(title="Creating History plot mode dropdown and text...") as _: 
        history_plot_dropdown = ui_options.create_dropdown(ui_options.HISTORYPLOT_OPTIONS)
        history_str = mo.md(f"History: {history_plot_dropdown} vs time") 

    return history_plot_dropdown, history_str


@app.cell(hide_code=True)
def _(mo, ui_options):
    # Plot mode profile Y coord dropdown ("profile_plot_dropdown") 
    with mo.status.spinner(title="Creating Profile plot mode dropdown...") as _: 
        profile_plot_dropdown = ui_options.create_dropdown(ui_options.PROFILEPLOT_OPTIONS) 

    return (profile_plot_dropdown,)


@app.cell(hide_code=True)
def _(mo, profile_xaxis_options, ui_options):
    # Plot mode profile x coord dropdown ("profile_plot_x_dropdown") 
    with mo.status.spinner(title="Creating Profile X Coord plot mode dropdown...") as _: 
        profile_plot_x_dropdown = ui_options.create_dropdown(profile_xaxis_options.PROFILEXAXIS_OPTIONS)

    return (profile_plot_x_dropdown,)


@app.cell(hide_code=True)
def _(
    comparison_mode_radio,
    helpers,
    mo,
    profile_plot_dropdown,
    profile_plot_x_dropdown,
    substage_selected,
    ui_options,
):
    # Plot mode profile string ("profile_str") which contains two dropdowns: "profile_plot_dropdown" and "profile_plot_x_dropdown" 

    with mo.status.spinner(title="Creating Profile plot mode text...") as _: 

        # Default values (if no substage is selected): Display an empty white line 
        substage_selected_str = "______" 
        substage_selected_color = "white"

        if comparison_mode_radio.value == ui_options.COMPAREMODE_MASSFIRST: 
            substage_selected_str = substage_selected.mode1_interior_plot_title 

        if comparison_mode_radio.value == ui_options.COMPAREMODE_STAGEFIRST: 
            substage_selected_str = substage_selected.mode2_interior_plot_title 

        # Text color of substage's name in the displayed text should match its flowchart color 
        if substage_selected: 
            substage_selected_color = substage_selected.flowchart_color 


        profile_str = mo.md(
            f"Interior profile: {profile_plot_dropdown} vs {profile_plot_x_dropdown} of a "
            f"{helpers.set_textcolor_css(substage_selected_str, substage_selected_color)} star" )





    return profile_str, substage_selected_color, substage_selected_str


@app.cell(hide_code=True)
def _(
    comparison_mode_radio,
    mo,
    mode1_massrange_dropdown,
    mode2_parentstage_dropdown,
    stellar_evolution_data,
    ui_options,
):
    # Identify available substages 

    with mo.status.spinner(title="Identifying available substages...") as _: 

        selected_massrange = [float(num) for num in mode1_massrange_dropdown.value.split('-')] 
        selected_parentstage = mode2_parentstage_dropdown.value 

        if comparison_mode_radio.value == ui_options.COMPAREMODE_NOSELECTION or comparison_mode_radio.value == ui_options.COMPAREMODE_FREE: 
            available_substages = []

        elif comparison_mode_radio.value == ui_options.COMPAREMODE_MASSFIRST: 
            available_substages = [
                s for s in stellar_evolution_data.SUBSTAGES_LIST 
                if not (s.mass_max <= selected_massrange[0] 
                        or s.mass_min >= selected_massrange[1])]

        elif comparison_mode_radio.value == ui_options.COMPAREMODE_STAGEFIRST: 
            available_substages = [
                s for s in stellar_evolution_data.SUBSTAGES_LIST 
                if s.parent_stage.name == selected_parentstage.name] 

    return available_substages, selected_massrange


@app.cell(hide_code=True)
def _(available_substages, comparison_mode_radio, helpers, mo, ui_options):
    # Create available substage tab selector (if there are any available substages)


    with mo.status.spinner(title="Creating substages selector...") as _: 

        if len(available_substages) == 0: 
            available_substages_tabs = "" 

        elif comparison_mode_radio.value == ui_options.COMPAREMODE_MASSFIRST: 

            available_substages_options = {
                helpers.set_textcolor_css(sub.mode1_abbrev, sub.flowchart_color): 
                sub.mode1_desc 
                for sub in available_substages}

            available_substages_tabs = mo.ui.tabs(
                available_substages_options, 
                value=list(available_substages_options.keys())[0]) 

        elif comparison_mode_radio.value == ui_options.COMPAREMODE_STAGEFIRST: 

            available_substages_options = {
                helpers.set_textcolor_css(sub.mode2_abbrev_with_massrange, sub.flowchart_color): 
                sub.mode2_desc_with_massrange 
                for sub in available_substages} 

            available_substages_tabs = mo.ui.tabs(
                available_substages_options, 
                value=list(available_substages_options.keys())[0]) 


    return (available_substages_tabs,)


@app.cell(hide_code=True)
def _(mo, stellar_evolution_data):
    # Create history browser free selection mode 

    with mo.status.spinner(title="Creating History data file browser...") as _: 

        history_browser = mo.ui.file_browser( 
            multiple=False, 
            selection_mode="directory", 
            restrict_navigation=True, 
            label="Choose MESA data folder", 
            initial_path=stellar_evolution_data.data_folder)


    return (history_browser,)


@app.cell(hide_code=True)
def _(history, mo):
    # Create profile dropdown for free selection mode 

    with mo.status.spinner(title="Creating Profile data dropdown selector...") as _: 

        if history is not None: 
            profile_dropdown = mo.ui.dropdown(
                label="Select Profile from the selected MESA data folder", 
                options=history.model_numbers_available) 
        else: 
            profile_dropdown = None 



    return (profile_dropdown,)


@app.cell(hide_code=True)
def _(
    available_substages_tabs,
    comparison_mode_radio,
    history_browser,
    mo,
    profile_dropdown,
    ui_options,
):
    # "model_selector": either use "available_substages_tabs" or an hstack of "history_browser" and "profile_dropdown", depending on value of "comparison_mode_radio" 

    with mo.status.spinner(title="Choosing model selector...") as _: 

        if comparison_mode_radio.value in [ui_options.COMPAREMODE_NOSELECTION, ui_options.COMPAREMODE_MASSFIRST, ui_options.COMPAREMODE_STAGEFIRST]: 
            model_selector = available_substages_tabs 
        if comparison_mode_radio.value == ui_options.COMPAREMODE_FREE: 
            model_selector = mo.hstack([history_browser.style(width="800px"), profile_dropdown], justify='space-around') 

    return (model_selector,)


@app.cell(hide_code=True)
def _(
    available_substages,
    available_substages_tabs,
    comparison_mode_radio,
    helpers,
    mo,
    ui_options,
):
    # Identify available substage tab that is currently selected (if there are any available substages)

    with mo.status.spinner(title="Identifying currently selected substage...") as _: 

        if len(available_substages) == 0: 
            substage_selected = None 

        elif comparison_mode_radio.value == ui_options.COMPAREMODE_MASSFIRST: 
            substage_selected = [
                s for s in available_substages 
                if helpers.set_textcolor_css(s.mode1_abbrev, s.flowchart_color) == available_substages_tabs.value
            ][0] 

        elif comparison_mode_radio.value == ui_options.COMPAREMODE_STAGEFIRST: 
            substage_selected = [
                s for s in available_substages 
                if helpers.set_textcolor_css(s.mode2_abbrev_with_massrange, s.flowchart_color) == available_substages_tabs.value
            ][0]

    return (substage_selected,)


@app.cell(hide_code=True)
def _(
    comparison_mode_radio,
    mo,
    selected_massrange,
    substage_selected,
    ui_options,
):
    # Identify model used to represent selected substage 

    with mo.status.spinner(title="Finding model to represent selected substage...") as _: 

        if substage_selected is None: 
            model_selected = None 

        elif len(substage_selected.models) == 0: 
            model_selected = None 

        elif comparison_mode_radio.value == ui_options.COMPAREMODE_MASSFIRST: 
            model_selected = next((m for m in substage_selected.models if selected_massrange[0]<=m.mass<=selected_massrange[1]), None)

        elif comparison_mode_radio.value == ui_options.COMPAREMODE_STAGEFIRST: 
            model_selected = next((m for m in substage_selected.models if m.is_default), substage_selected.models[0])

    return (model_selected,)


@app.cell(hide_code=True)
def _(
    Path,
    comparison_mode_radio,
    history_browser,
    load_data,
    mo,
    model_selected,
    ui_options,
):
    # Load selected history 

    with mo.status.spinner(title="Loading MESA history file...") as _: 

        if model_selected is not None: 
            history = load_data.load_history(model_selected.MESA_folder_path)
        elif comparison_mode_radio.value == ui_options.COMPAREMODE_FREE: 
            if len(history_browser.value) > 0: 
                history = load_data.load_history(Path(history_browser.value[0].id))
            else: 
                history = None 
        else: 
            history = None


    return (history,)


@app.cell(hide_code=True)
def _(
    Path,
    history,
    history_browser,
    load_data,
    mo,
    model_selected,
    profile_dropdown,
):
    # Load selected profile 

    with mo.status.spinner(title="Loading MESA profile file...") as _: 

        if model_selected is not None: 
            modelnum = model_selected.model_example 
            profile = load_data.load_profile(model_selected.MESA_folder_path, modelnum, history) 

        elif profile_dropdown is not None and profile_dropdown.value is not None: 
            modelnum = profile_dropdown.value 
            profile = load_data.load_profile(Path(history_browser.value[0].id), modelnum, history)

        else: 
            modelnum = None 
            profile = None 

    return modelnum, profile


@app.cell(hide_code=True)
def _(
    available_substages,
    comparison_mode_radio,
    stellar_evolution_data,
    ui_options,
):
    # Create list of all unique models 


    if comparison_mode_radio.value==ui_options.COMPAREMODE_MASSFIRST: 

        # Create an empty dictionary to store the unique models.
        # The keys will be the unique folder paths, and the values will be the model objects.
        unique_models_dict = {}

        # Loop through all substages and all their associated models
        for substage in stellar_evolution_data.SUBSTAGES_LIST:
            for model in substage.models:
                # If we haven't seen this folder path before...
                if model.MESA_folder_path not in unique_models_dict:
                    # ...add the model object to our dictionary.
                    unique_models_dict[model.MESA_folder_path] = model

        # You now have a dictionary where each value is a unique SubStageModel object.
        # You can get a list of just the objects by using .values()
        unique_models_list = list(unique_models_dict.values())



    elif comparison_mode_radio.value==ui_options.COMPAREMODE_STAGEFIRST: 

        unique_models_list = [] 
        for _substage in available_substages: 
            if len(_substage.models) == 0: 
                continue 
            _model = next((m for m in _substage.models if m.is_default), _substage.models[0])
            unique_models_list.append(_model) 


    else: 
        unique_models_list = [] 


    return (unique_models_list,)


@app.cell
def _(
    HR_diagram_plotting,
    available_substages,
    comparison_mode_radio,
    flowchart_switch,
    flowchart_yaxis_dropdown,
    lru_cache,
    mo,
    mpatches,
    np,
    plt,
    selected_massrange,
    stellar_evolution_data,
    substage_selected,
    ui_options,
    unique_masses,
):
    # Draw the flowchart

    import matplotlib.ticker as mticker 


    def draw_substage_box(
        ax, substage, 
        bg_color, bg_alpha, 
        border_linewidth, border_color, 
        text_color, text_fontsize, text_y=None):

        # Define rectangle bounds
        x1 = substage.parent_stage.flowchart_x + 0.05 
        x2 = substage.parent_stage.flowchart_x+1 - 0.05  
        y1 = substage.mass_min
        y2 = substage.mass_max
        width = x2 - x1
        height = y2 - y1

        # Add the rectangle
        rect = mpatches.Rectangle(
            (x1, y1), width, height,
            linewidth=border_linewidth,
            edgecolor=border_color,
            facecolor=bg_color, 
            alpha=bg_alpha, 
        )
        ax.add_patch(rect)

        # Add text inside the rectangle 
        if text_y is None: 
            text_y = np.sqrt(y1*y2)
        ax.text(
            x1 + width/2, text_y, #np.sqrt(y1*y2),
            substage.flowchart_text,
            ha='center', va='center',
            fontsize=text_fontsize, color=text_color
        )




    # Function to draw the flowchart, updating highlights/labels based on selection
    @lru_cache(maxsize=32) 
    def draw_flowchart():

        # Allow flowchart to be minimized 
        if flowchart_switch.value == False: 
            return "Flowchart minimized by user" 

        # If the user is freely selecting a MESA file, minimize the flowchart 
        if comparison_mode_radio.value==ui_options.COMPAREMODE_FREE: 
            return "Flowchart unavailable"

        fig, ax = plt.subplots(figsize=(15, 5))
        fig.subplots_adjust(top=0.95, bottom=0.16, left=0.07, right=0.92)

        if comparison_mode_radio.value==ui_options.COMPAREMODE_NOSELECTION: 
            custom_yticks = unique_masses 
            custom_xtick_labels = [parent_stage.short_name for parent_stage in stellar_evolution_data.ParentStage]

        if comparison_mode_radio.value==ui_options.COMPAREMODE_MASSFIRST: 
            custom_yticks = [selected_massrange[0], selected_massrange[1]] 
            custom_xtick_labels = [
                parent_stage.short_name 
                if parent_stage in [stage.parent_stage for stage in available_substages] 
                else "" 
                for parent_stage in stellar_evolution_data.ParentStage
            ]

        if comparison_mode_radio.value==ui_options.COMPAREMODE_STAGEFIRST: 
            custom_yticks = sorted({m for substage in available_substages for m in (substage.mass_min, substage.mass_max)})
            custom_xtick_labels = [
                parent_stage.short_name 
                if parent_stage in [stage.parent_stage for stage in available_substages] 
                else "" 
                for parent_stage in stellar_evolution_data.ParentStage
            ]

        # Y axis: Mass
        ax.set_ylabel("Mass", fontsize=18, labelpad=14)
        ax.set_ylim(min(unique_masses), max(unique_masses))
        ax.set_yscale("log")

        if flowchart_yaxis_dropdown.value==1: 
            HR_diagram_plotting.label_spectraltypes(ax, location="right", attribute="mass", subtype_fraction_threshold=0.5, min_subtype_label_px=30)   
            # custom_yticks = [] 
            # ax.yaxis.set_minor_formatter(mticker.NullFormatter())
            # ax.set_ylabel("Spectral Type (on MS)", fontsize=18, labelpad=40) 

        ax.set_yticks(custom_yticks)
        ax.set_yticklabels([str(tick) for tick in custom_yticks], fontsize=14)
        ax.tick_params(axis="y", which="minor", length=0)
        for y in custom_yticks:
            ax.axhline(y, color="black", lw=0.5, ls=(0, (4, 3.6123)), zorder=0)

        # X axis: Evolution
        ax.set_xlabel("Evolutionary phase", fontsize=18, labelpad=14)
        ax.set_xlim(0, 9)
        custom_xticks = np.arange(0, len(stellar_evolution_data.ParentStage)) + 0.5
        ax.set_xticks(custom_xticks)
        ax.set_xticklabels(custom_xtick_labels, fontsize=14)


        if comparison_mode_radio.value==ui_options.COMPAREMODE_NOSELECTION: 
            for substage in stellar_evolution_data.SUBSTAGES_LIST: 
                draw_substage_box(
                    ax, 
                    substage, 
                    bg_color=substage.flowchart_color, 
                    bg_alpha=1.0, 
                    border_color="black", 
                    border_linewidth=1, 
                    text_color="black", 
                    text_fontsize=12, 
                )


        if comparison_mode_radio.value==ui_options.COMPAREMODE_MASSFIRST: 
            for substage in available_substages: 
                if substage.id == substage_selected.id: 
                    draw_substage_box(
                        ax, 
                        substage, 
                        bg_color=substage.flowchart_color, 
                        bg_alpha=1.0, 
                        border_color="black", 
                        border_linewidth=2, 
                        text_color="black", 
                        text_fontsize=12, 
                        text_y=np.sqrt(selected_massrange[0]*selected_massrange[1])
                    ) 
                else: 
                    draw_substage_box(
                        ax, 
                        substage, 
                        bg_color=substage.flowchart_color, 
                        bg_alpha=0.2, 
                        border_color="black", 
                        border_linewidth=1, 
                        text_color="black", 
                        text_fontsize=12, 
                        text_y=np.sqrt(selected_massrange[0]*selected_massrange[1])
                    )


        if comparison_mode_radio.value==ui_options.COMPAREMODE_STAGEFIRST: 
            for substage in available_substages: 
                if substage.id == substage_selected.id: 
                    draw_substage_box(
                        ax, 
                        substage, 
                        bg_color=substage.flowchart_color, 
                        bg_alpha=1.0, 
                        border_color="black", 
                        border_linewidth=2, 
                        text_color="black", 
                        text_fontsize=12 
                    ) 
                else: 
                    draw_substage_box(
                        ax, 
                        substage, 
                        bg_color=substage.flowchart_color, 
                        bg_alpha=0.2, 
                        border_color="black", 
                        border_linewidth=1, 
                        text_color="black", 
                        text_fontsize=12, 
                    ) 


        return mo.mpl.interactive(fig)





    with mo.status.spinner(title="Drawing flowchart...") as _: 
        flowchart = draw_flowchart()

    return (flowchart,)


@app.cell(hide_code=True)
def _(
    HR_diagram_plotting,
    comparison_mode_radio,
    history,
    history_plot_dropdown,
    load_data,
    lru_cache,
    mo,
    model_selected,
    modelnum,
    plot_mode_radio,
    profile,
    profile_plot_dropdown,
    profile_plot_x_dropdown,
    profile_plotting,
    substage_selected_color,
    substage_selected_str,
    ui_options,
    unique_models_list,
):
    # Create figure showing interior plot 






    @lru_cache(maxsize=32) 
    def create_fig2(): 



        # HR Diagram 
        if plot_mode_radio.value == ui_options.PLOTMODE_HRDIAGRAM: 

            if history is None: 
                return "Select a History file to view HR diagram" 

            hr = HR_diagram_plotting.HRDiagram() 

            for model in unique_models_list: 
                history_new = load_data.load_history(model.MESA_folder_path) 

                if comparison_mode_radio.value==ui_options.COMPAREMODE_STAGEFIRST: 
                    color=model.parent_substage.flowchart_color 
                elif comparison_mode_radio.value==ui_options.COMPAREMODE_MASSFIRST: 
                    color=None

                if history_new.star_mass[0] == history.star_mass[0]: 
                    hr.add_path(history, label=f"{history.star_mass[0]:.1f} $M_{{sun}}$", color=color) 
                    continue

                hr.add_path(history_new, label=f"{history_new.star_mass[0]:.1f} $M_{{sun}}$", alpha=0.3, color=color) 

            if model_selected is not None: 
                color = model_selected.parent_substage.flowchart_color
            else: 
                color = None 

            if len(unique_models_list)==0: 
                hr.add_path(history, label=f"{history.star_mass[0]:.1f} $M_{{sun}}$", color=color) 

            hr.add_modelnum_labels(history, modelnum)         
            HR_diagram_plotting.label_spectraltypes(hr.ax) 
            hr.legend() 
            fig2 = hr.fig 
            return mo.mpl.interactive(fig2) 



        # History plots 
        if plot_mode_radio.value == ui_options.PLOTMODE_HISTORY: 

            if history is None: 
                return "Select a History file to view history plot" 

            selected_plot_func = history_plot_dropdown.value.plot_func 
            fig2 = selected_plot_func(history, modelnum_now=modelnum) 

            # history_plotting.add_substage_highlight(fig2, model_selected, history) 
            return mo.mpl.interactive(fig2) 



        # Interior profile plots 
        if plot_mode_radio.value == ui_options.PLOTMODE_PROFILE:

            if history is None or profile is None: 
                return "Select a Profile file to view profile plot" 

            # Create profile plot depending on selected options in dropdown 
            selected_plot_func = profile_plot_dropdown.value.plot_func 
            selected_x_axis = profile_plot_x_dropdown.value  
            fig2 = selected_plot_func(profile, selected_x_axis, history)

            # List of strings used in the title (i.e., "Interior composition of a" + "Subgiant" (with red text) + "star")
            profile_str = profile_plot_dropdown.value.title_str
            title_str_list = [profile_str, substage_selected_str, "star"]  

            # List of colors used in title (i.e., "black" + "red" + "black") 
            title_colors_list = ['black', substage_selected_color, 'black'] 

            # Add colored region to title 
            if comparison_mode_radio.value != ui_options.COMPAREMODE_FREE: 
                profile_plotting.add_colored_title(fig2, title_str_list, title_colors_list, fontsize=20) 
            return mo.mpl.interactive(fig2) 





    with mo.status.spinner(title="Drawing secondary plot...") as _: 

        secondary_plot = create_fig2() 








    return (secondary_plot,)


@app.cell(hide_code=True)
def _():
    # Imports/setup 

    import marimo as mo



    with mo.status.spinner(title="Importing packages...") as _: 

        # Standard packages 
        import os 
        import numpy as np 
        from pathlib import Path 
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches
        import matplotlib.colors as mcolors 
        from functools import lru_cache 

        # Nonstandard packages 
        import mesa_reader as mr 

        plt.style.use('default') # Make sure the plots appear with a white background, even if the user is in dark mode 


    return Path, lru_cache, mo, mpatches, np, plt


@app.cell(hide_code=True)
def _(mo):
    with mo.status.spinner(title="Importing packages...") as _: 
        import utils.load_data as load_data 
        import utils.helpers as helpers 
    return helpers, load_data


@app.cell(hide_code=True)
def _(mo):
    with mo.status.spinner(title="Importing packages...") as _: 
        import utils.plotting.history_plotting as history_plotting 
        import utils.plotting.profile_plotting as profile_plotting 
        import utils.plotting.HR_diagram_plotting as HR_diagram_plotting
    return HR_diagram_plotting, profile_plotting


@app.cell(hide_code=True)
def _(mo):
    with mo.status.spinner(title="Importing packages...") as _: 
        import utils.config.stellar_evolution_data as stellar_evolution_data 
        import utils.config.ui_options as ui_options 
        import utils.config.profile_xaxis_options as profile_xaxis_options 
    return profile_xaxis_options, stellar_evolution_data, ui_options


@app.cell
def _(
    HR_diagram_str,
    comparison_mode_radio,
    comparison_mode_title,
    controls_subtitle,
    flowchart,
    flowchart_subtitle_hstack,
    freeselection_str,
    full_title,
    history_str,
    massfirst_str,
    mo,
    model_selector,
    noselection_str,
    plot_mode_radio,
    plot_mode_title,
    profile_str,
    secondary_plot,
    secondary_plot_subtitle,
    stagefirst_str,
    userguide_subtitle_hstack,
    userguide_text,
):
    # MAIN 


    full_interface = mo.vstack(
        [
            full_title, 
            "\u200b", 
            mo.md("---"), 
            "\u200b", 

            userguide_subtitle_hstack, 
            userguide_text, 
            "\u200b", 
            mo.md("---"), 
            "\u200b", 

            controls_subtitle, 
            plot_mode_title, 
            mo.hstack(
                [
                    plot_mode_radio, 
                    mo.vstack(
                        [
                            HR_diagram_str, 
                            history_str, 
                            profile_str
                        ], 
                        gap=0)
                ], 
                gap=0, align="center"), 
            "\u200b", 

            comparison_mode_title, 
            mo.hstack(
                [
                    comparison_mode_radio, 
                    mo.vstack(
                        [
                            noselection_str, 
                            massfirst_str, 
                            stagefirst_str, 
                            freeselection_str
                        ], 
                        gap=0)
                ], 
                gap=0, align="center"), 
            "\u200b", 
            model_selector, 
            "\u200b", 
            mo.md("---"), 
            "\u200b", 

            flowchart_subtitle_hstack, 
            flowchart, 
            "\u200b", 
            mo.md("---"), 
            "\u200b", 

            secondary_plot_subtitle, 
            secondary_plot, 
            "\u200b", 
            mo.md("---"), 

        ], 
        gap=0.7 
    ) 


    full_interface 



    return


if __name__ == "__main__":
    app.run()
