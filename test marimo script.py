import marimo

__generated_with = "0.13.15"
app = marimo.App(width="medium")


@app.cell
def _():
    # data_folder = Path("C:/Users/johnm/Local Desktop/Gayley/MESA output files/")

    return


@app.cell
def _():
    # Goal: Rewrite loading data functions 

    import marimo as mo 
    import matplotlib.pyplot as plt 
    import time 






    return mo, plt


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
def _(mo, plt):

    fig, ax = plt.subplots(figsize=(15, 5))  # Set width and height in inches
    ax.plot([1, 2])
    mo.mpl.interactive(fig)
    return


if __name__ == "__main__":
    app.run()
