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
        print '%vn is not found!' %vn
        return False

#
# touch play
#
def play(vc):
    # android.widget.ImageButton com.spotify.music:id/btn_play
    vn   = 'btn_play' # vn: view name
    vid  = package + ":id/" + vn

    view = vc.findViewById(vid)

    if view:
        print '"%s" touch!' %vid
        view.touch()
        return True
    else:
        print '"%s" is not found' %vn
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
# main screen dispatch
#
def Playing(vc,scmd): # scmd: screen command

    '''
    try:
        vc.dump()
    except RuntimeError as e:
        print '[ERROR] %s' %e
        sys.exit()
    '''

    vc.dump()

    if scmd == SCMD_TITLE:
        ret,title = getTitle(vc)
        return ret,title
    elif scmd == SCMD_CONNECT:
        return connect(vc)
    elif scmd == SCMD_PLAY:
        return play(vc)
    else:
        pass
