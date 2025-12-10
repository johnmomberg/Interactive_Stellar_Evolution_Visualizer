# Interactive Stellar Evolution Visualizer

## Quick Start

- Click here to load the tool in your browser:
  https://marimo.app/github.com/johnmomberg/Interactive_Stellar_Evolution_Visualizer/blob/main/main.py 
- To hide the code, click the button with **three boxes** in the bottom-right corner of the screen.

## How to give feedback  

There are several ways that you can give feedback (report a bug, make suggestions, etc):
- Add an issue to this repository’s **Issues** tab.  
- Email me at john-momberg@uiowa.edu 
- Fill out this survey about your experience using this program:  
  https://docs.google.com/forms/d/e/1FAIpQLSfM8DIz6Jri5ruX6axiyvR9M9x5XapsTQQrbQr-yVbNdOL2TA/viewform?usp=header 

--- 

## Detailed Walkthrough / User Guide 

### Controls 
To use this tool, first make a selection using the Controls section. Depending on the options you select, the corresponding plot will be generated and displayed in the Plot section below. 

#### 1. Choose variable to plot 
Select the type of plot you want to generate:

- **HR diagram**: Shows the star’s path across the HR diagram. 
- **History**: a variable vs. time (e.g., radius vs. time). 
- **Interior profile**: interior structure (variable vs. location inside the star) at a snapshot in time.

For **Interior profile**, you can additionally select the units used on the x-axis: 
- **Radius**: Distance from the center (standard) 
- **Mass coordinate**: The amount of mass interior to each point. (For example, 'x = 1.5' means the location in the star where a sphere extending to your current radius would contain a total of 1.5 solar masses). 

#### 2. Choose type of star 
This tool emphasizes the ability to make comparisons. There are two types of comparisons students might want to make: 

- A: Compare one star at different points in its life
- B: Compare stars of different masses at the same point in their lives

In order to allow for both types of comparison, the way that you select a star depends on what you want to compare it to. Before selecting a star, you must choose a "comparison mode" from the following options: 

##### A. Select *mass* first
Use this when you want to follow one star through its evolution. (For example: for a 1.0 solar mass star, how does the star change from the main sequence to the red giant phase?) 

1. First, select a **mass range** from the dropdown. 
2. The UI will show the evolutionary stages your selected mass goes through. (Different masses go through different stages, so the options displayed will depend on your previous selection.) 
3. Next, choose an **evolutionary stage** from the tabs that appear.  

Use this mode to answer the question: *"How does a particular star change over time?"*

##### B. Select *stage* first
Use this to compare how a particular evolutionary stage is experienced by stars of different masses. (For example: during the main sequence, what is the difference between a low-mass star and a high-mass star?) 

1. First, select an **evolutionary stage** from the dropdown.  
2. The UI will display which mass ranges have distinct behavior during that stage. (Different stages have different mass ranges where distinct behavior occurs, so the options displayed will depend on your previous selection.)
3. Next, choose a **mass range** from the tabs that appear.

Use this mode to answer the question: *“How do stars of different masses look at this particular stage?”*

##### C. Free exploration

This tool also functions as a general MESA file explorer. Rather than viewing types of stars in the context of their evolutionary stage ("main sequence", "red giant", "low mass", "high mass", etc), you can instead directly select the MESA file you would like to visualize. 

1. Use the File Browser to select a MESA folder. To select a folder, click on the icon to the left of its name. (Don't click the folder name; that enters the folder) 
2. Once a MESA folder has been selected, choose a specific point in time. Each point in time that can be selected is given a "model number" or "modelnum", which simply tells the program which MESA file to load. (Model numbers are used because models are not spaced linearly in time; more models are created during times where the star changes rapidly, and fewer models are created during times where the star goes long periods of time without changing.)

##### Upload your own MESA folder 

You can upload MESA run in order to apply the visualizations I've created to your own data. 

1. A proper MESA folder should contain 'history.data' or 'trimmed_history.data' and a sequence of profile files like 'profile1.data', 'profile2.data', etc.  
2. Compress your MESA folder (right-click -> compress to .zip) 
3. Click **Upload** and select your .zip MESA folder

After uploading, the folder may not immediately appear in the file browser. To fix this, follow these steps to refresh the file browser: 
1. Click the special folder **“Click HERE to refresh file browser”** to enter it.  
2. Inside is another fake folder labeled **“Click Back Arrow to refresh file browser”**. This folder simply exists so that its title instructs you what to do next: Click the **back arrow** to return to the parent folder.  
3. Entering and leaving a subfolder forces the file browser to refresh, and your uploaded folder should now be visible.

--- 

## Acknowledgements 

---






























# More notes and rougher drafts 

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



---



Original notes/rough draft: 


How to use this program 

1. Choose variable to plot Choose the type of plot to generate. Options include:
   a. HR diagram: Shows the path that the star takes across the HR diagram
   b. History: something vs time. Example: Radius vs time.
   c. Interior profile: Interior structure, or something vs location within the star, at a fixed age. For the profile plot, there are two options for what you can plot on the x axis:
   1. Radius: Exactly what you would expect to be plotted on the x axis of a plot showing the interior structure of a star.
   2. 2. Mass coordinate: This represents however much mass is contained inside the point shown. So if x=0.3, that corresponds to the location in the star where you've travelled far enough out from the center such that 0.3 solar masses is interior to your current radius.

2. Choose type of star This program emphasizes the use of understanding by making comparisons. There are two types of comparisons that can be made, and which comparison mode you are considering affects which button in this selector you choose.
   1. For a given star, compare its properties at different points in its life (for instance, from main sequence to red giant). This corresponds to the button label "Select mass first". The idea is that you select the mass first, then the program tells you what evolutionary stages that THAT particular mass goes through, and then you select the evolutionary stage second. First, select the mass range from the dropdown. Depending on your selection, the program will tell you which stages that mass range goes through. Second, make a selection on the tabs selector that appears to choose an evolutionary stage.
   2. For a given point in time, compare how stars of different masses experience it (for instance, compare the properties during the main sequence of a low mass star vs a high mass star). This corresponds to the button labeled "Select stage first". The idea is that first, you pick the evolutionary stage (for example, main sequence), and the program tells you what ranges of masses do different things during that stage (for instance maybe 1.5 solar masses is hte cutoff between different behavior in the main sequence) so you pick your stage first and then pick the mass range. First, select the evolutionary stage using the dropdown. Depending on your selection, the program will display which ranges of masses do different things during this evolutionary stage. Second, make your selection on the tabs selector that appears in order to choose a mass range.
   3. Free exploration: Modes 1 and 2 were the main ways this program is meant to be used: I have associated each stage of stellar evolution/type of star with a MESA file and assigned a specific point in time that I think represents that stage best. However, if you want to see how the star behaves at points in between the time steps I've higlighted, or you just want to explore the data more freely, you can use the Free Exploration mode. This allows you to directly select the MESA file to load and then select the exact point in time you would like to view; in this mode, points in time are just as they come from the MESA folder, and I haven't imposed my own definitions of when the "main sequence" or "red giant" branch occurs. To select a folder to analyze, click the folder icon to the left of the name (a checkmark should appear in the box). Do not click the name of the folder; this causes you to go INTO the folder but you aren't actually selecting it for analysis. Next, once you've selected a MESA folder to analyze, you can pick a particular point in time within this MESA file using the dropdown selector. Model numbers, or "modelnums", are a way that MESA labels different points in time (since it might create more models in a short period of time if a lot of change happens so its not linear with time). The age of the star at each point is also included next to where I label the modelnum.

This mode also allows you to upload your OWN mesa data folder for analysis. You can upload your own folder and use all of my interactive features and plots and use this tool to visualize and browse data of your own. To do that, click the Upload button and select a .zip compressed version of your MESA data folder. A MESA data folder should contain: "trimmed_history.data" or "history.data", and a series of files that looks like "profile1.data", "profile2.data", etc. If you take a MESA data folder and right click and compress to .zip, then you can upload it to my program to be plotted. After uploading, your folder may not appear in the file browser. If so, you must refresh the file browser. In order to do this, you must enter a folder and then go back to the parent folder. To accomplish this, I added a fake folder called "Click HERE to refresh file browser". You can click the name of that folder to enter it. Inside, you will see a fake folder called "Click Back Arrow to refresh file browser". The title of this folder instructs you to click the back arrow, returning you to the parent folder. This manuever is my hacked way of forcing you to refresh the file browser, and you should now see the folder that you uploaded listed. You can click on the box next toyour folder to select it just as you can select any other MESA data folder. 

Flowchart 
Below the controls section, you will see the Evolutionary Flowchart. This diagram summarizes the stages of life that stars of different masses go through. Intitial mass is given on the y axis. For a given value of mass, you can move along horizontally to see what stages that mass evolves into. The x axis lists out all of the major evolutionary stages. NOTE: This is NOT linear with respect to time. If it was, the main sequence would take up 99% of the lifetime of most stars. In addition, the main sequence for lower mass stars would be longer for lower mass stars, so you woudn't even be able to see the data for high mass stars. Instead, the flowchart uses "evolutionary stage" as a kind of proxy for age. Each evolutionary stage is sometimes broken into smaller sub-regions meaning stars of different masses experience that stage in different ways. For example, all stars go through the main sequence, but the properties of the main sequence are different for stars above and below 1.5 solar masses, so I'm representing that difference by creating a separation between the two boxes there. When in mode 1 (select mass first), all of the evolutionary stages in a horizontal line, that correspond to the selected mass, are highlighted, showing how you can compare different points in time of this mass. If you're in mode 2 (select stage first), boxes in a vertical line are highlighted, corresponding to the selected evolutionary stage, showing how you can compare how stars of different masses experience a particular stage of evolution. The right side of the flowchart gives the spectral type of a star with the corresponding mass when it's on the main sequence. NOTE: This is not necessarily the spectral type of the star at all points in its life. In fact, it will certainly change spectral type; for example, when stars become red giants, they would all become spectral type M. Instead, this allows you to better understand what is meant when someone talks about the evolution of "B type stars" or "G type stars" or "B3 type stars" or whatever. What that means is "the evolution of a star that, when its on the main sequence, has a spectral type of B", and the question is, what MASS does that correspond to? So I added a spectral type on MS axis to the right side of the plot to answer this question. 

Plot 
The selected plot is generated for the selected type of star and is displayed below the flowchart."

