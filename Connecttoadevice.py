#
# find the device in id/device_list
#
# tddn: target device display name
def find_device(vc,vop,tddn):
    vn       = 'devices_list' # vn: view name
    vid_type = VID_TYPE_NAME
    return view_list_op(vc,vn,vid_type,vop,tddn)

#
#
#
def open_connection_type(vc,vop,tddn): # tddn: tgt_device_display_name

    # firstly find and return view if the device in the device_list
    # so, specified VOP_VIEW
    view = find_device(vc,VOP_VIEW,tddn) 

    if not view:
        print '[ERROR] "%s": Can\'t get view information TextView in "%s"' %(tddn,TXT_CTAD)
        return False
    else:
        vtext = tddn
        view  = view_op(vc,vtext,VID_TYPE_TEXT,VOP_VIEW)

        if view is None:
            print '[ERROR] "%s": Can\'t get view information TextView in "%s"' %(vtext,TXT_CTAD)
            return False
        else:
            idstr         = view.getUniqueId()
            ret,vidtddnno = pick_idno(idstr) # vidtddnno: view id tddn no

            if ret == False:
                print '[ERROR] Can\'t idno %s for %s' %(idstr,vtext)
                return False
            else:
                vibtn_found = None
                # ctidno : connect type(ImageButton "...") id no
                # assume ImageButton id no = tddn view id no + 1 or 2
                for i in range(1,3):
                    vidibtnno  = str(vidtddnno + i) # vidibtnno: view id ImageButton no
                    vidibtnstr = 'id/no_id/' + vidibtnno

                    vibtn = vc.findViewById(vidibtnstr) # vibtn: view ImageButton
                    if vibtn.getClass() in 'android.widget.ImageButton':
                        vibtn_found = True
                        vibtn.touch()
                        return True
                    else:
                        pass

                if vibtn_found:
                    print '[INFO] found ImageButton(connection_type) for %s in "device_list"' %tddn
                else:
                    print '[ERROR] Can\'t get view information "ImageButton ..." in "device_list"'
                    return False

#
# connecting
#
# tddn: target device display name
def connecting_check(vc,tddn):

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
            if   tddn              in connect_text:
                cs = CONNECT_STATUS_CONNECTED
            elif 'Devices Available' in connect_text:
                cs = CONNECT_STATUS_CANNOT_CONNECTED
            elif 'Connecting'        in connect_text: # connect_text is 'Connecting' + gomi
                pass
            else:
                pass
        elif cs == CONNECT_STATUS_CONNECTED:
            print '[INFO] "%s" is connected' %tddn
            break
        elif cs == CONNECT_STATUS_CANNOT_CONNECTED:
            print '[INFO] "%s" is not connected' %tddn
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
def change_connection_type(vc,arg):

    if connection_status.has_key(arg):
        view = vc.findViewWithText(arg)
        if view is None:
            return False
        else:
            view.touch()
    else:
        return False

#
#
#
def Connecttoadevice(vc,scmd,vop,arg=None): # scmd: screen command

    vc.dump()

    if   scmd == SCMD_DEVICE:
        return find_device(vc,vop,arg)
    elif scmd == SCMD_OPEN_CONNECTION_TYPE:
        return open_connection_type(vc,vop,arg)
    elif scmd == SCMD_GET_CONNECTION_INFO_ALL:
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
