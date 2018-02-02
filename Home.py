#
# touch btn_connect
#
def connect(vc,vop):
    # btn_connect
    # android.widget.TextView com.spotify.music:id/btn_connect
    vn       = 'btn_connect' # vn: view name
    vid_type = VID_TYPE_NAME
    return view_op(vc,vn,vid_type,vop)

#
# touch ImageButton playPause
#
def playPause(vc,vop):
    # 'android.widget.ImageButton com.spotify.music:id/playPause'
    vn       = 'playPause' # vn: view name
    vid_type = VID_TYPE_NAME
    return view_op(vc,vn,vid_type,vop)

#
# Title
#
def getTitle(vc):
    # android.widget.TextView com.spotify.music:id/glue_toolbar_title Home
    idstr1 = 'com.spotify.music:id/glue_toolbar_title'
    view1  =  vc.findViewById(idstr1)
        
    idstr2 = 'com.spotify.music:id/context_title'
    view2  =  vc.findViewById(idstr2)

    if view1:
        return True,view1.getText()
    elif view2:
        return True,view2.getText()
    else:
        return False,None

#
# Title
#
def your_library_tab(vc,vop):
    vn       = 'your_library_tab' # vn: view name
    vid_type = VID_TYPE_NAME
    return view_op(vc,vn,vid_type,vop)

#
#
#
def settings(vc,vop):
    idno     = '4'
    vid_type = VID_TYPE_NO
    return view_op(vc,idno,vid_type,vop)

#
#
#
def home_tab(vc,vop):
    vn       = 'home_tab' # vn: view name
    vid_type = VID_TYPE_NAME
    return view_op(vc,vn,vid_type,vop)

#
# main screen dispatch
#
def Home(vc,scmd,vop=None): # scmd: screen command

    vc.dump()

    if scmd == SCMD_TITLE:
        ret,title = getTitle(vc)
        return ret,title
    elif scmd == SCMD_CONNECT:
        return connect(vc,vop)
    elif scmd == SCMD_PLAYPAUSE:
        return playPause(vc,vop)
    elif scmd == SCMD_YOUR_LIBRARY_TAB:
        return your_library_tab(vc,vop)
    elif scmd == SCMD_SETTINGS:
        return settings(vc,vop)
    elif scmd == SCMD_HOME_TAB:
        return home_tab(vc,vop)
    else:
        pass

