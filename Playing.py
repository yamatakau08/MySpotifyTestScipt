#
# touch btn_connect
#
def connect(vc):
    vn       = 'btn_connect' # vn: view name
    vid_type = VID_TYPE_NAME
    return view_op(vc,vn,vid_type,vop)

#
# touch play
#
def play(vc):
    vn   = 'btn_play' # vn: view name
    vid_type = VID_TYPE_NAME
    return view_op(vc,vn,vid_type,vop)

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
