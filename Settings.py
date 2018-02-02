#
# 
#
def find_setting(vc,vop,arg):
    vn       = 'list' # vn: view name
    vid_type = VID_TYPE_NAME
    return view_list_op(vc,vn,vid_type,vop,arg,vpackage='android')

'''
def xfind_setting(vc,vop,arg):

    vn    = 'list' # vn: view name
    # lview: list view
    lview = view_op(vc,vn,VID_TYPE_NAME,VOP_VIEW,vpackage='android')

    if lview.scrollable():
        # refer AndroidViewClient-13.6.2/src/com/dtmilano/android/viewclient.py line 2045
        ATTEMPTS = 4
        for i in range(ATTEMPTS):
            view = vc.findViewWithText(arg)
            if view:
                break
            else:
                lview.uiScrollable.flingForward()
                vc.sleep(1)
                vc.dump()
    else:
        view = vc.findViewWithText(arg)

    if view:
        print '[INFO] "%s" found in "%s"' %(arg,vn)
        if vop == VOP_TOUCH:
            view.touch()
            return True
        if vop == VOP_EXIST:
            return True
        else:
            print '[ERROR] vop:"%s" is not supported in find_device()!' %(vop)
            return False
    else:
        print '[ERROR] "%s" not found in "%s"' %(arg,vn)
        return False
'''

#
# main screen dispatch
#
def Settings(vc,scmd,vop,arg=None): # scmd: screen command

    vc.dump()

    if scmd == SCMD_SETTING:
        return find_setting(vc,vop,arg)
    elif scmd == SCMD_PLAYPAUSE:
        return playPause(vc,vop)  # defined in Home.py
    elif scmd == SCMD_HOME_TAB:
        return home_tab(vc,vop)   # defined in Home.py
    else:
        pass
