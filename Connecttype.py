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
        print '[INFO] sleep %ssec for checking connection sutatus:%s' %(ssec,cs)
        tsleep(ssec)
        vc.dump()
    
        # android.widget.TextView com.spotify.music:id/btn_connect
        vn       = 'btn_connect' # vn: view name
        vid_type = VID_TYPE_NAME
        view = view_op(vc,vn,vid_type,VOP_VIEW)

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
            print '[INFO] "%s" is connected' %device
            break
        elif cs == CONNECT_STATUS_CANNOT_CONNECTED:
            print '[INFO] "%s" is not connected' %device
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
                                            #exist #view  #connection status
    connection_info = {GOOGLE_CAST:        [None,  None, False],
                       SPOTIFY_CONNECT:    [None,  None, False],
                       FORGET_THIS_DEVICE: [None,  None, False]}

    flag_gs = False # flag_gs: _gs: Cast/Connect

    for k,v in connection_info.items():
        view = vc.findViewWithText(k)

        if not view: # view not exist
            value = connection_info[k]
            value[0] = None
            value[1] = None
            value[2] = False
        else: # view exist
            value = connection_info[k]

            # value[0]: exist in list
            value[0] = True

            # value[1]: view
            value[1] = view

            # value[2]: connection status
            if k == 'Google Cast' or k == 'Spotify Connect': # need to check if there is ImageView shows connect
                vidnostr  = view.getUniqueId() # vidnostr: view id no string
                ret,vidno = pick_idno(vidnostr)
                vidselimg = 'id/no_id/' + str(vidno + 1) # vidselimg: view id selected image +1: assume next id selected is image view?
                viv = vc.findViewById(vidselimg) # viv: view ImageView

                if viv and viv.getClass() == 'android.widget.ImageView':
                    value[2] = True
                    flag_gs  = True
                else:
                    value[2] = False
                        
    if not flag_gs:
        v = connection_info[FORGET_THIS_DEVICE]
        # connection status
        v[2] = True
        
    if scmd == SCMD_GET_CONNECTION_INFO_ALL:
        return True,connection_info
    elif scmd == SCMD_GET_CONNECTION_INFO_NOW:
        for k,v in connection_info.items():
            if v[2] == True:
                return True,k
        return False,None
    elif scmd == SCMD_CHANGE_CONNECTION_TYPE:
        if arg in connection_info.keys():
            v = connection_info[arg]
            v[1].touch()
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
