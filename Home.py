#
# touch btn_connect
#
def connect(vc):
    # btn_connect
    # android.widget.TextView com.spotify.music:id/btn_connect
    vn   = 'btn_connect' # vn: view name
    vid  = package + ":id/" + vn
    view = vc.findViewById(vid)
    if view:
        view.touch()
        return True
    else:
        print '[ERROR] %vn is not found!' %vn
        return False

#
# touch ImageButton playPause
#
def playPause(vc):
    # 'android.widget.ImageButton com.spotify.music:id/playPause'
    vn   = 'playPause' # vn: view name
    vid  = package + ":id/" + vn

    view =  vc.findViewById(vid)
    
    if view:
        view.touch()
        return True
    else:
        print "[ERROR] %s is not found!" %vn
        return False

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
def your_library_tab(vc):
    vn   = 'your_library_tab' # vn: view name
    vid  = package + ":id/" + vn
    view = vc.findViewById(vid)

    if view:
        view.touch()
        return True
    else:
        print '[ERROR] %vn is not found!' %vn
        return False

#
#
#
def settings(vc):

    vmap = vc.getViewsById()
    vid = 'id/no_id/4' # vid: view id
    view = vmap[vid]

    if view:
        view.touch()
        return True
    else:
        print '[ERROR] %s is not found!' %vn
        return False

#
#
#
def home_tab(vc):

    vn  = 'home_tab' # vid: view id
    vid = package + ":id/" + vn
    view = vc.findViewById(vid)

    if view:
        view.touch()
        return True
    else:
        print '[ERROR] %s is not found!' %vn
        return False

#
# main screen dispatch
#
def Home(vc,scmd): # scmd: screen command

    vc.dump()

    if scmd == SCMD_TITLE:
        ret,title = getTitle(vc)
        return ret,title
    elif scmd == SCMD_CONNECT:
        return connect(vc)
    elif scmd == SCMD_PLAYPAUSE:
        return playPause(vc)
    elif scmd == SCMD_YOUR_LIBRARY_TAB:
        return your_library_tab(vc)
    elif scmd == SCMD_SETTINGS:
        return settings(vc)
    elif scmd == SCMD_HOME_TAB:
        return home_tab(vc)
    else:
        pass

