#
# common lib(function)
#
def printViewsById(vc):
    dict_ids = vc.getViewsById() # getViewsById returns dict type
    for k, v in dict_ids.items():
        print k,dict_ids[k]
    return dict_ids

def vcsleep(sec):
    print 'ViewClient.sleep(%s)' %sec
    ViewClient.sleep(sec)

def tsleep(sec):
    print 'time.sleep(%s)' %sec
    time.sleep(sec)

def debug():
    import pdb; pdb.set_trace()    

def pick_idno(idstr):
    # idstr assume the following style
    # 'id/no_id/16'
    arr  = idstr.split('/')
    size = len(arr)
    if size > 0 :
        # asuume arr[size-1] the last element is 'no' itself
        if arr[size-1].isdigit():
            return True, int(arr[size-1])
        else:
            return False
    else:
        return False

#
#
#
# vid_type
(
    VID_TYPE_NO,
    VID_TYPE_NAME,
    VID_TYPE_TEXT,
) = range(0,3)

(
    VOP_TOUCH,
    VOP_ENABLED,
    VOP_EXIST,
    VOP_VIEW, # return view instace if it's exist
) = range(0,4)

# vop: view operation
# vpackage: view package
#           need to select android/package itself
def view_op(vc,vid,vid_type,vop,vpackage=None,debug=True):

    xvid = None
    view = None

    # check view type no/name/text
    if   vid_type == VID_TYPE_NO:
        vmap = vc.getViewsById()
        xvid = 'id/no_id/' + vid
        if vmap.has_key(xvid):
            view = vmap[xvid]
        else:
            print '[ERROR] vid_type:%s vid:"%s" is not in the list by getViewsById()!' %(vid_type,xvid)
            return False
    elif vid_type == VID_TYPE_NAME:
        if vpackage:
            xvid = vpackage + ":id/" + vid
        else:
            xvid = package + ":id/" + vid

        view = vc.findViewById(xvid)
    elif vid_type == VID_TYPE_TEXT:
        xvid = vid
        view = vc.findViewWithText(vid)
    else:
        print '[ERROR] vid_type:"%s" for "%s" is not supported!' %(vid_type,xvid)
        return False

    # check if view is exist
    if view:
        if   vop == VOP_TOUCH:
            view.touch()
            return True
        elif vop == VOP_ENABLED:
            return view.enabled()
        elif vop == VOP_EXIST:
            return True
        elif vop == VOP_VIEW:
            return view
        else:
            print '[INFO] "%s" for "%s" is not supported!' %(vop_type,xvid)
            return True
    else:
        if debug:
            print '[ERROR] view:"%s" is not found!' %(xvid)

        if vop == VOP_VIEW:
            return None

        return False

# vid: id str/name/text
# vop: view operation
# vpackage: view package
#           need to select android/package itself
def view_list_op(vc,vid,vid_type,vop,arg=None,vpackage=None,debug=True):

    xvid = None
    view = None

    # check view type no/name/text
    if   vid_type == VID_TYPE_NO:
        vmap = vc.getViewsById()
        xvid = 'id/no_id/' + vid
        if vmap.has_key(xvid):
            view = vmap[xvid]
        else:
            print '[ERROR] vid_type:%s vid:"%s" is not in the list by getViewsById()!' %(vid_type,xvid)
            return False
    elif vid_type == VID_TYPE_NAME:
        if vpackage:
            xvid = vpackage + ":id/" + vid
        else:
            xvid = package + ":id/" + vid

        view = vc.findViewById(xvid)
    elif vid_type == VID_TYPE_TEXT:
        xvid = vid
        view = vc.findViewWithText(vid)
    else:
        print '[ERROR] vid_type:"%s" for "%s" is not supported!' %(vid_type,xvid)
        return False

    # check if view is exist
    if view:
        if view.scrollable():
            # refer AndroidViewClient-13.6.2/src/com/dtmilano/android/viewclient.py line 2045
            ATTEMPTS = 4
            for i in range(ATTEMPTS):
                tview = vc.findViewWithText(arg) # tview: text view
                if tview: # found!
                    view = tview
                    break
                else:
                    view.uiScrollable.flingForward()
                    vc.sleep(1)
                    vc.dump()
        else:
            pass

        return view_op(vc,arg,VID_TYPE_TEXT,vop)

    else:
        if debug:
            print '[ERROR] view:"%s" is not found!' %(xvid)

        if vop == VOP_VIEW:
            return None

        return False
    
