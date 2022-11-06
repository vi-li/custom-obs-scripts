# custom-obs-scripts
Collection of custom OBS scripts for personal use and sharing.

Contents:
* [auto-show-hide-window.py](#auto-show-hide-windowpy)

---

### auto-show-hide-window.py
Automates the showing and hiding of a specific scene item so you don't have to manually click the "eye" button every time you switch to and from a certain application. Works on Windows OS only, since it uses the libaries `win32gui` and `win32process`. (Adapted from [xantyleonhart](https://github.com/xantyleonhart/obs-scripts/blob/main/hidewindow.py))

Properties:
- **Enabled (boolean)**: Checked if you want the script to be functioning, unchecked if not.
- **Latency (ms) (int)**: The cadence at which you want the polling to occur. Lower latency means higher responsiveness, but may cause lag (especially in debug mode).
- **Scene (string)**: Which scene you want this functionality to work on. Currently, you can only specify one scene at a time.
- **Source (string)**: Which source you want to show/hide. Currently, you can only specify one source at a time.

Limitations:
- **WIP**: Seems to cause some kind of memory leak. Need to fix.
- Script only works on one scene and one source at the moment.
- Source needs to be named the same thing as its application .exe at the moment.

---

I hope you find some usefulness in my efforts!
Thanks, have a great day :)
