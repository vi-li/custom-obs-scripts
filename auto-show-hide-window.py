# github.com/vi-li

import obspython as obs
import win32gui as wgui
import win32process as wprocess
import psutil

enabled = True
interval = 500
source_name = ""
scene_name = ""
description = "Enables/Disables window capture source (with transitions) when the window gets/loses focus"
debug_mode = True

def script_defaults(settings):
    global enabled
    global interval
    global s_handler
    global source_name
    global scene_name
    global debug_mode

    if debug_mode: print("Called script defaults")

    obs.obs_data_set_default_int(settings, "interval", interval)
    obs.obs_data_set_default_bool(settings, "enabled", enabled)

seen_history = {'second_last_seen': None,
                'last_seen': None }

#returns window_id of the new window when changing windows, -1 otherwise
def curr_focused():
    global debug_mode
    if debug_mode: print("Called curr_focused")
    try:
        # Get exe name from foreground window id
        _, active_window_pid = wprocess.GetWindowThreadProcessId(wgui.GetForegroundWindow())
        active_exe = psutil.Process(active_window_pid).name()
        if debug_mode: print("Active exe: ", active_exe)

        if (seen_history['last_seen'] is None or active_exe != seen_history['last_seen']):
            if debug_mode: print('** New executable seen, id: ', active_exe)
            seen_history['second_last_seen'] = seen_history['last_seen']
            seen_history['last_seen'] = active_exe
            return active_exe
    except:
        pass

    return ""


# Make visible source if its window is focused, make invisible otherwise
# Calls both show and hide transitions
def update_window():
    global debug_mode
    if not enabled:
        return

    if debug_mode: print("Called update_window")
    current_exe = curr_focused()
    if debug_mode: print("Current executable name: ", seen_history['last_seen'], "Source window name: ", source_name)
    if (current_exe is not "" and source_name is not ""):
        source = obs.obs_get_source_by_name(source_name)
        scene = obs.obs_get_scene_by_name(scene_name)
        sceneitem = obs.obs_scene_sceneitem_from_source(scene, source)

        if debug_mode:
            print("Source: ", source)
            print("Scene: ", scene)
            print("Scene item: ", sceneitem)

        if (current_exe == source_name):
            isVisible = True
            if debug_mode: print('- Show: ', source_name)
            obs.obs_source_set_enabled(source, isVisible)
            obs.obs_sceneitem_set_visible(sceneitem, isVisible)
            obs.obs_sceneitem_do_transition(sceneitem, isVisible)

        elif (seen_history['second_last_seen'] == source_name):
            isVisible = False
            if debug_mode: print('- Hide: ', source_name)
            obs.obs_sceneitem_set_visible(sceneitem, isVisible)
            obs.obs_sceneitem_do_transition(sceneitem, isVisible)

        obs.obs_source_release(source)
        obs.obs_sceneitem_release(sceneitem)
        obs.obs_scene_release(scene)

#Update source info
def update_source(calldata=None): 
    global debug_mode
    if debug_mode: print("Called update_source")
    global source_name
    # Get source by name
    source = obs.obs_get_source_by_name(source_name)
    if debug_mode: print("Attempting to get settings of: ", source_name)
    # Get window properties from the source (window id)
    props = obs.obs_source_get_settings(source)
    if debug_mode: print("Updated source: ", source_name)
    obs.obs_source_release(source)
    obs.obs_data_release(props)

# ------------------------------------------------------------

def script_description():
    global debug_mode
    if debug_mode: print("Called description")
    return description


# Called each time script properties are modified
def script_update(settings):
    global enabled
    global interval
    global source_name
    global scene_name
    global debug_mode
    if debug_mode: print("Called script_update")

    # Disconnect callbacks from old source
    disconnect_callbacks()

    # Set old source visible
    source = obs.obs_get_source_by_name(source_name)
    obs.obs_source_set_enabled(source, True)
    obs.obs_source_release(source)

    # Update variables with the new property values
    enabled     = obs.obs_data_get_bool(settings, "enabled")
    interval    = obs.obs_data_get_int(settings, "interval")
    source_name = obs.obs_data_get_string(settings, "source")
    scene_name  = obs.obs_data_get_string(settings, "scene")
    
    # Connect callbacks to new source
    connect_callbacks()
    update_source()

    # Create a timer that calls update function periodically
    obs.timer_remove(update_window)
    obs.timer_add(update_window, interval)

# Definition of script properties to be shown on the GUI
def script_properties():
    global debug_mode
    if debug_mode: print("[CS] Loaded properties.")

    props = obs.obs_properties_create()

    obs.obs_properties_add_bool(props, "enabled", "Enabled")
    obs.obs_properties_add_int(props, "interval", "Latency (ms)", 250, 5000, 50)
    
    s = obs.obs_properties_add_list(props, "scene", "Scene", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
    scenes = obs.obs_frontend_get_scene_names()
    if scenes is not None:
        for scene in scenes:
            obs.obs_property_list_add_string(s, scene, scene)

    p = obs.obs_properties_add_list(props, "source", "Source", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
    sources = obs.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_type = obs.obs_source_get_unversioned_id(source)
            if source_type == "window_capture":
                name = obs.obs_source_get_name(source)
                obs.obs_property_list_add_string(p, name, name)

    obs.source_list_release(sources)

    return props

##Callbacks--------------------------------------------------------------------------

def connect_callbacks():
    global debug_mode
    if debug_mode: print("Binding to " + source_name)
    source = obs.obs_get_source_by_name(source_name)
    sh = obs.obs_source_get_signal_handler(source)
    obs.signal_handler_connect(sh, "save", update_source)
    # if debug_mode: obs.signal_handler_connect_global(sh, onActivate)
    obs.obs_source_release(source)

def disconnect_callbacks():
    global debug_mode
    if debug_mode: print("Unbinding to " + source_name)
    source = obs.obs_get_source_by_name(source_name)
    sh = obs.obs_source_get_signal_handler(source)
    obs.signal_handler_disconnect(sh, "save", update_source)
    # if debug_mode: obs.signal_handler_connect_global(sh, onDeactivate)
    obs.obs_source_release(source)

# Debug events
#def onActivate(e,calldata):
    # source = obs.calldata_source(calldata,"source")
    # print('\n activated')

#def onDeactivate(e,calldata):
    # source = obs.calldata_source(calldata,"source")
    # print('\n deactivated')

# Subscribe on_load callback
def script_load(settings):
    global debug_mode
    if debug_mode: print("[CS] Loaded script.")
    print("Hi! This script is written by vi-li on GitHub, jellyl3mon on Twitch.\nHave a nice day! :)")
    print("Currently, there are some limitations.\nYou must name the source you want to show/hide the same as its executable name (ex. chrome.exe for Google Chrome).")
    obs.obs_frontend_add_event_callback(on_load)

# Waits until frontend is loaded to get source data. Otherwise, it may get empty reference.
def on_load(event):
    global debug_mode
    if debug_mode: print("Called on_load")
    if event == obs.OBS_FRONTEND_EVENT_FINISHED_LOADING:
        connect_callbacks()
        update_source()