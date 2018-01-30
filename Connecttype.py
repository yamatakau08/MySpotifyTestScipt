#
# connecting
#
def connecting_check(vc,device): # device: string

    CONNECT_STATUS_CONNECTING        = 3 # "Connecting..."
    CONNECT_STATUS_CONNECTED         = 4 # Connected displaying model name
    CONNECT_STATUS_CANNOT_CONNECTED  = 5 # cannot connected

    cs = CONNECT_STATUS_CONNECTING
    ssec = 3;

    while True:
        print 'sleep %ssec for checking connection sutatus:%s' %(ssec,cs)
        tsleep(ssec)
        vc.dump()
    
        # android.widget.TextView com.spotify.music:id/btn_connect
        vn  = 'btn_connect' # vn: view name
        vid = package + ":id/" + vn

        print vid

        view = vc.findViewById(vid)

        if view:
            connect_text = view.getText()
        else:
            print '[ERROR] Can\'t get view %s' %vn
            return

        print '[INFO] connect_text: %s' %connect_text

        if cs == CONNECT_STATUS_CONNECTING:
            if   device              in connect_text:
                cs = CONNECT_STATUS_CONNECTED
            elif 'Devices Available' in connect_text:
                cs = CONNECT_STATUS_CANNOT_CONNECTED
            elif 'Connecting'        in connect_text: # connect_text is 'Connecting' + gomi
                pass
            else:
                pass
        elif cs == CONNECT_STATUS_CONNECTED:
            print '"%s" is connected' %device
            break
        elif cs == CONNECT_STATUS_CANNOT_CONNECTED:
            print '"%s" is not connected' %device
            break
        else:
            pass
        
#
#
#
def Connection(vc,scmd,arg=None): # scmd

    GOOGLE_CAST        = 'Google Cast'
    SPOTIFY_CONNECT    = 'Spotify Connect'
    FORGET_THIS_DEVICE = 'Forget this device'

    connection_status = {GOOGLE_CAST:        None,
                         SPOTIFY_CONNECT:    None,
                         FORGET_THIS_DEVICE: None,}
    connection_view   = {GOOGLE_CAST:        None,
                         SPOTIFY_CONNECT:    None,
                         FORGET_THIS_DEVICE: None,}

    # check if 'Forget this device', firstly
    # sometimes 'Forget this dvice' is not in list
    view = vc.findViewWithText(FORGET_THIS_DEVICE)
    if view:
        connection_status[FORGET_THIS_DEVICE] = True
    else:
        del connection_status[FORGET_THIS_DEVICE]
        
    # check if each connection type has ImageView shows the current connectio type 
    for k,v in connection_status.items():
        view = vc.findViewWithText(k)

        if view is None:
            connection_status[k] = False
        else:
            connection_view[k] = view

            vidnostr  = view.getUniqueId() # vidnostr: view id no string
            ret,vidno = pick_idno(vidnostr)
            vidselimg = 'id/no_id/' + str(vidno + 1) # vidselimg: view id selected image +1: assume next id selected is image view?
            viv = vc.findViewById(vidselimg) # viv: view ImageView

            if viv and viv.getClass() == 'android.widget.ImageView':
                connection_status[k] = True
            else:
                connection_status[k] = False

    if scmd == SCMD_GET_CONNECTION_INFO_ALL:
        return True,connection_status
    elif scmd == SCMD_GET_CONNECTION_INFO_NOW:
        for k,v in connection_status.items():
            if v == True:
                return True,k
        return False,None
    elif scmd == SCMD_CHANGE_CONNECTION_TYPE:
        if arg in connection_status.keys():
            connection_view[arg].touch()
            return True,arg
        else:
            return False,None
    else:
        pass

#
#
#
def Connecttype(vc,scmd,arg): # scmd: screen command

    vc.dump()

    if scmd == SCMD_GET_CONNECTION_INFO_ALL:
        ret,cinfo = Connection(vc,scmd,arg) # cinfo: connection_info
        return ret,cinfo
    elif scmd == SCMD_GET_CONNECTION_INFO_NOW:
        ret,cinfo = Connection(vc,scmd,arg) # cinfo: connection_info
        return ret,cinfo
    elif scmd == SCMD_CHANGE_CONNECTION_TYPE:
        ret,cinfo = Connection(vc,scmd,arg) # cinfo: connection_info
        return ret,cinfo
    else:
        pass
