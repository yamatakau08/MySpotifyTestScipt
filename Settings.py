#
# 
#
def find_setting(vc,arg,touch=None):

    ATTEMPTS = 4

    # refer AndroidViewClient-13.6.2/src/com/dtmilano/android/viewclient.py line 2045
    for i in range(ATTEMPTS):
        android___id_list = vc.findViewByIdOrRaise("android:id/list")
        view = vc.findViewWithText(arg)
        if view:
            print '"%s" found in "Settings"' %arg
            if touch:
                view.touch()
            return True
        else:
            android___id_list.uiScrollable.flingForward()
            vc.sleep(1)
            vc.dump()

    print '[ERROR] "%s" not found in "Settings"' %arg
    return False

#
# main screen dispatch
#
def Settings(vc,scmd,arg=None): # scmd: screen command

    vc.dump()

    if scmd == SCMD_FIND_SETTING:
        return find_setting(vc,arg)
    if scmd == SCMD_SELECT_SETTING:
        return find_setting(vc,arg,touch=True)
    elif scmd == SCMD_PLAYPAUSE:
        return playPause(vc)  # defined in Home.py
    elif scmd == SCMD_HOME_TAB:
        return home_tab(vc)   # defined in Home.py
    else:
        pass

