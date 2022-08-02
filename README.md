# custom-obs-scripts
Collection of custom OBS scripts for personal use and sharing.

Contents:
* [auto-show-hide-window.py](#auto-show-hide-windowpy)

---

### auto-show-hide-window.py
A script I wrote to automate the showing and hiding of a specific scene item so I wouldn't have to manually click the "eye" button every time I switched to and from a certain window. (Adapted from [xantyleonhart](https://github.com/xantyleonhart/obs-scripts/blob/main/hidewindow.py))

Properties:
- **Enabled (boolean)**: Checked if you want the script to be functioning, unchecked if not.
- **Latency (ms) (int)**: The cadence at which you want the polling to occur. Lower latency means higher responsiveness, but may cause lag (especially in debug mode).
- **Scene (string)**: Which scene you want this functionality to work on. Currently, you can only specify one scene at a time.
- **Source (string)**: Which source you want to show/hide. Currently, you can only specify one source at a time.

---

I hope you find some usefulness in my efforts!
Thanks, have a great day :)
