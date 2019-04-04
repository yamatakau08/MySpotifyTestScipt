#
# 
#
def find_setting(vc,vop,arg):
    vn       = 'list' # vn: view name
    vid_type = VID_TYPE_NAME
    return view_list_op(vc,vn,vid_type,vop,arg,vpackage='android')

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
