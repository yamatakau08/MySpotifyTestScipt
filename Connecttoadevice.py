#
# find the device in id/device_list
#
def find_device(vc,arg,touch=None): # arg tgt_device_display_name:

    ATTEMPTS = 4

    # refer AndroidViewClient-13.6.2/src/com/dtmilano/android/viewclient.py line 2045
    for i in range(ATTEMPTS):
#       android___id_list = vc.findViewByIdOrRaise("android:id/list")
        android___id_list = vc.findViewByIdOrRaise("com.spotify.music:id/devices_list")
        view = vc.findViewWithText(arg)
        if view:
            print '"%s" found in "%s"' %(arg,TXT_CTAD)
            if touch:
                view.touch()
            return True
        else:
            android___id_list.uiScrollable.flingForward()
            vc.sleep(1)
            vc.dump()

    print '[ERROR] "%s" not found in "%s"' %arg,TXT_CTAD
    return False

#
#
#
def select_device(vc,tddn): # tddn: tgt_device_display_name:
    vtext = tddn # vtext: view text
    view  = vc.findViewWithText(vtext)

    if view:
        print '"%s" found in "%s" list' %(vtext,TXT_CTAD)
        print '"%s" selected' %vtext
        view.touch()
        return True
    else:
        print '[ERROR] "%s" not found in "%s" list' %(vtext,TXT_CTAD)
        return False

#
# first implementation 
#
def drag(vc):
    vid = 'com.spotify.music:id/devices_list' # vid: view id
    devices_list = vc.findViewById(vid)

    # refer https://stackoverflow.com/questions/17520956/scrolling-list-using-android-view-clientdtmilano/17540116#17540116
    #    (x,y,w,h) = devices_list.getPositionAndSize()
    (x,y,w,h) = devices_list.getPositionAndSize()
    print 'x:%d y:%d w:%d h:%d' %(x,y,w,h) # Xperia Z3 returns x:0 y:75 w:1080 h:1536

    # drag
    start = (int(x+w/2.0),y+h-y)
    end   = (int(x+w/2.0),y+y)
    vc.device.drag(start,end,200)
    # vc.traverse() # need?

    '''
    # http://www.howtobuildsoftware.com/index.php/how-do/bnk1/android-python-androidviewclient-implement-infinite-scrolling-in-androidviewclient
    def doSomething(view):
        if view.getClass() == 'android.widget.TextView':
            print view.getText()

    # check if scrollable
    if devices_list.isScrollable():
        vc.traverse(root=devices_list, transform=doSomething)
        print "Scrolling"
        device.dragDip((185.0, 499.0), (191.0, 175.5), 200, 20, 0) # ambiguos
    '''
#
#
#
def open_connection_type(vc,tddn): # tddn: tgt_device_display_name

    views = vc.getViewsById()

    vtext = tddn # vtext: view text
    view  = vc.findViewWithText(vtext)
    if view is None:
        print '[ERROR] "%s": Can\'t get view information TextView in "%s"' %(vtext,TXT_CTAD)
        return False
    else:
        idstr = view.getUniqueId()

    ret,vidtddnno = pick_idno(idstr) # vidtddnno: view id tddn no

    if ret == False:
        print '[ERROR] Can\'t idno %s for %s' %(idstr,vtext)
        return False
    else:
        # ctidno : connect type(ImageButton "...") id no
        # + 1 or 2    : ImageButton id no = tddn view id no + 2
        for i in range(1,3):
            vidibtnno = str(vidtddnno + i) # vidibtnno: view id ImageButton no
            vidibtnstr = 'id/no_id/' + vidibtnno

            vibtn = vc.findViewById(vidibtnstr) # vibtn: view ImageButton
            if vibtn is None:
                print '[ERROR] Can\'t get view information "ImageButton ..." in "device_list" view'
                return False
            else:
                if vibtn.getClass() in 'android.widget.ImageButton':
                    vibtn.touch()
                    return True

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
def Connecttoadevice(vc,scmd,arg): # scmd: screen command

    vc.dump()

    if   scmd == SCMD_FIND_DEVICE:
        return find_device(vc,arg)
    elif scmd == SCMD_SELECT_DEVICE:
        return find_device(vc,arg,touch=True)
    elif scmd == SCMD_OPEN_CONNECTION_TYPE:
        return open_connection_type(vc,arg)
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
