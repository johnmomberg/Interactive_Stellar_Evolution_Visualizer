import marimo

__generated_with = "0.13.15"
app = marimo.App(width="medium")


@app.cell
def _():
    # data_folder = Path("C:/Users/johnm/Local Desktop/Gayley/MESA output files/")

    return


@app.cell
def _():
    # # Goal: Rewrite loading data functions 

    # import marimo as mo 
    # import matplotlib.pyplot as plt 
    # import time 






    return


@app.cell
def _():
    # # Hello 
    # print("Hey")
    # mo.refs()
    return


@app.cell
def _():
    # test_dropdown = mo.ui.dropdown(options=["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]) 
    # # test_dropdown 
    return


@app.cell
def _():
    # # mo.vstack([test_dropdown, mo.status.spinner(remove_on_exit=False) if loading==True else mo.md("Done!")]) 
    # test_dropdown 
    return


@app.cell
def _():

    # with mo.status.spinner(title="Loading...") as spinner: 
    #     time.sleep(1) 
    #     x = test_dropdown.value 
    #     time.sleep(1) 

    return


@app.cell
def _():

    # fig, ax = plt.subplots(figsize=(15, 5))  
    # ax.plot([1, 2])
    # mo.mpl.interactive(fig)
    return


@app.cell
def _():
    # # Setup 
    # fig, ax = plt.subplots(figsize=(12.8, 7))
    # fig.subplots_adjust(top=0.82, bottom=0.13, left=0.10, right=0.81)


    # # X axis: Temperature 
    # ax.set_xlabel("Surface temperature (K)", fontsize=18, labelpad=14)
    # ax.set_xscale("log")
    # ax.set_xlim((80000, 1000)) 


    # # Y axis: Luminosity 
    # ax.set_ylabel("Luminosity ($L_{{sun}}$)", fontsize=18, labelpad=14)
    # ax.set_yscale("log")
    # ax.set_ylim((1e2, 1e4))


    # # Grid, ticks, title 
    # ax.tick_params(labelsize=14, length=10, which="major") 
    # # ax.grid(alpha=0.5, which="both")
    # ax.set_title("Evolutionary Path Across HR Diagram", fontsize=20, pad=15) 

    # mo.mpl.interactive(fig)
    return


@app.cell
def _():
    import src 
    import marimo as mo 
    import matplotlib.pyplot as plt 
    plt.style.use('default')



    hr = src.plot.hr.hr.HRDiagram()  

    for mass in [0.2]: 
        history = src.load_data.load_history(src.data.file_paths.MESA_data_folder/f"M={mass}")
        hr.add_path(history, label=mass) 

    hr.legend(fontsize=12, loc="center left", bbox_to_anchor=(1, 0.5)) 
    hr.add_spectral_type_labels()  

    mo.mpl.interactive(hr.fig)







    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
