# Interactive Stellar Evolution Visualizer

## Quick Start

- Click here to load the tool in your browser:
  https://marimo.app/github.com/johnmomberg/Interactive_Stellar_Evolution_Visualizer/blob/main/main.py 
- To hide the code, click the button with **three-rectangle** in the bottom-right corner of the screen.

## Feedback 

There are several ways that you can give feedback (report a bug, make suggestions, etc):
- Add an issue to this repository’s **Issues** tab.  
- Email: john-momberg@uiowa.edu 
- Fill out this short survey:  
  https://docs.google.com/forms/d/e/1FAIpQLSfM8DIz6Jri5ruX6axiyvR9M9x5XapsTQQrbQr-yVbNdOL2TA/viewform?usp=header 

---



# WARNING: ChatGPT generated content below (I will edit and adapt this later)


## How to use the program

### 1. Choose the kind of plot
Select the type of plot you want to generate:

- **HR diagram** — the star’s path across the HR diagram.  
- **History** — a variable vs. time (e.g., radius vs. time).  
- **Interior profile** — a snapshot of interior structure (variable vs. location inside the star) at a **specific** evolutionary time.

For **Interior profile** you can choose the x-axis unit:

- **Radius** — distance from center (what you usually expect for interior plots).  
- **Mass coordinate** — the fraction (or amount) of mass interior to that radius (e.g., `x = 0.3` means 0.3 M\_☉ is inside that radius).

---

### 2. Choose the type of comparison (how you pick mass/stage)
This program emphasizes comparative exploration. There are three modes — pick the one that matches the comparison you want:

#### A. **Select mass first** (compare different times for a single mass)  
Use this when you want to follow one star through its evolution (e.g., main sequence → red giant):

1. Select a **mass range** from the dropdown.  
2. The UI will show the evolutionary stages that mass goes through.  
3. Choose an **evolutionary stage** from the tabs that appear.  
4. The profile plot (if requested) will show the star at the point in time used to represent that stage.

This mode answers: *“How does this particular star change over time?”*

#### B. **Select stage first** (compare different masses at one stage)  
Use this to compare how stars of different masses behave at the same evolutionary stage (e.g., the main sequence):

1. Select an **evolutionary stage** from the dropdown.  
2. The UI will display which mass ranges have distinct behavior in that stage.  
3. Choose a **mass range** from the tabs that appear.

This mode answers: *“How do stars of different masses look at this particular stage?”*

#### C. **Free exploration** (select exact models / times)  
If you want finer control (e.g., points between the highlighted stages), use Free Exploration:

- Select a specific MESA model folder, then pick the **exact model number** (modelnum) you want to inspect.  
- Each `modelnum` corresponds to a saved model snapshot; its age is shown next to the modelnum so you know the star’s age at that snapshot.  
- This mode does **not** use the pre-selected stage definitions — it shows the raw model timesteps exactly as they appear in the MESA output.

---

### Upload your own MESA data
You can upload a `.zip` of your own MESA run and use the visualizer with your data:

- A proper MESA folder should contain `history.data` or `trimmed_history.data` and a sequence of profile files like `profile1.data`, `profile2.data`, etc.  
- Zip the MESA folder (right-click → compress → `.zip`) and click **Upload** in the app.  
- After uploading, the folder may not appear immediately — refresh the file browser:
  1. Click the special folder **“Click HERE to refresh file browser”** to enter it.  
  2. Inside is another fake folder labeled **“Click Back Arrow to refresh file browser”**. Click the back arrow to return to the parent folder.  
  3. This forces a refresh and your uploaded folder should then be visible.  
- Select the checkbox next to your folder (don’t click the folder name — that opens it instead of selecting it).

---

## Flowchart (evolutionary overview)

Below the controls you’ll find an **Evolutionary Flowchart**:

- **Y axis** = initial mass.  
- **X axis** = evolutionary stages (this axis is *not* linear in time).  
- Move horizontally for a fixed initial mass to see that star’s sequence of stages over time.  
- Move vertically to compare different masses at the same evolutionary stage.  
- Each stage may be split into subregions to show qualitatively different behavior (e.g., main sequence behavior can differ above/below ~1.5 M\_☉).  
- The right side of the flowchart shows **main-sequence spectral type** for each mass — this denotes the spectral type that star *has on the main sequence*, not its type at later stages (giants will change type).

---

## The generated plot
The selected plot is created for the chosen star/type and configuration and is displayed below the flowchart. Use the available plot controls to toggle axes (log/linear), invert (e.g., HR diagrams often invert the temperature axis), and save images.

---

## Tips & common issues

- **Profile plots require both a mass and an evolutionary stage.**  
  A profile is a snapshot at a single time — if you select only a mass but no stage, the profile plot will be unavailable. In that case you will see an error message instructing you to pick a stage from the tabs. (History plots can be shown with just a mass.)

- **Model numbering (modelnum):** MESA saves many snapshots and labels them with `modelnum`. These are not evenly spaced in time. The displayed age next to each `modelnum` helps you pick the exact epoch.

- **If an uploaded folder doesn’t show up:** perform the file-browser refresh (see *Uploading MESA data*).

---

## Data format / expectations
A valid MESA data folder should include:

- `history.data` or `trimmed_history.data`  
- Profile files named like `profile1.data`, `profile2.data`, etc.

If the file structure differs, the app may not detect the run correctly.

---

## Troubleshooting messages (examples)

- **Profile plot unavailable: please select both a mass and an evolutionary stage.**  
  _Reason:_ Profiles are tied to a specific time. Select a stage (tab) after choosing a mass, or use Free Exploration to pick a modelnum directly.

- **Uploaded folder not visible:** follow the File Browser refresh steps in *Uploading MESA data*.

---

## Contact & collaboration
If you’d like to collaborate, test features, or contribute MESA models, I’m eager to hear from you:

- Email: **john-momberg@uiowa.edu**  
- Open an issue on GitHub for specific feature requests or bugs.

---

## License & citation
*(Add your preferred license text here or a short citation instruction if you’d like people to cite your work when they use it.)*
