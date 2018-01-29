#! /usr/bin/env python

import re
import sys
import os
import string
import time

try:
    sys.path.append(os.path.join(os.environ['ANDROID_VIEW_CLIENT_HOME'], 'src'))
except:
    pass

from com.dtmilano.android.viewclient import UiDevice
from com.dtmilano.android.viewclient import ViewClient

# the device name which support "Spotify Connect"
TGT_DEVICE_DISPLAY_NAME = 'SRSyama'

execfile('Home.py')
execfile('Playing.py')
execfile('DeviceList.py')

TXT_CTAD = 'Connect to a device'

#
#
#
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
def printViewsById(vc):
    dict_ids = vc.getViewsById() # getViewsById returns dict type
    for k, v in dict_ids.items():
        print dict_ids[k]
    return dict_ids

# https://qiita.com/everycamel/items/470abe67d83db5140f55
# enum smething for screen command
(
# Main/Playing
    SCMD_TITLE,
    SCMD_CONNECT,
    SCMD_PLAY,
    SCMD_PLAYPAUSE,
# DEVICE_LIST    
    SCMD_FIND_DEVICE,
    SCMD_SELECT_DEVICE,
    SCMD_OPEN_CONNECTION_TYPE,
    SCMD_GET_CONNECTION_INFO_ALL,
    SCMD_GET_CONNECTION_INFO_NOW,
    SCMD_CHANGE_CONNECTION_TYPE,
) = range(0,10) # (0,X) X: total number of elements

def vcsleep(sec):
    print 'ViwewClient.sleep(%s)' %sec
    ViewClient.sleep(sec)

def tsleep(sec):
    print 'time.sleep(%s)' %sec
    time.sleep(sec)

def debug():
    import pdb; pdb.set_trace()    

#
# following is main
#
package   = 'com.spotify.music'
activity  = '.MainActivity'
component = package + "/" + activity

device, serialno = ViewClient.connectToDeviceOrExit()


if device.isLocked():
    print '[ERROR] Screen is Locked!'
    sys.exit()

print 'Start component:"%s"' %component
device.startActivity(component=component)

vc = ViewClient(device, serialno) # vc: ViewClient Music Center
uidevice =UiDevice(vc)

# it will fail to set English(United States) "en-rUS" when Language setting is other than "Japanese"
# 
# it will fail to search Language & input when settings in "Japanese"
# languageTo is defined in viewclient.py
# uidevice.changeLanguage(languageTo="en-rUS") # 
# uidevice.openQuickSettingsSettings()

# check android.widget.TextView com.spotify.music:id/glue_toolbar_title
ret,title = Home(vc,SCMD_TITLE)
if ret:
    print 'Now screen title: "%s"' %title
else:
    print 'main screen is not found'
    print 'Is screen locked?'
    sys.exit()

if not title == 'Playing from Playlist':
    # touch btn_connect in MAIN SCREEN
    print 'Touch btn_connect to open "Playing from .*"'
    Home(vc,SCMD_CONNECT)
    # screen will be 'Playing from .*'
    ret,title = Playing(vc,SCMD_TITLE)
    if ret and 'Playing from' in title:
        print 'Screen is "%s"' %title
    else:
        print 'Screen is not "Playing from .*" tilte:%s"' %title

while True:
    # touch btn_connect
    print 'touch btn_connect to open "%s"' %TXT_CTAD
    Playing(vc,SCMD_CONNECT)

    DeviceList(vc,SCMD_OPEN_CONNECTION_TYPE,TGT_DEVICE_DISPLAY_NAME)
    ret,cinfo = DeviceList(vc,SCMD_GET_CONNECTION_INFO_ALL,TGT_DEVICE_DISPLAY_NAME) # cinfo: connection info
    if ret:
        print 'connection type(list): %s' %cinfo
    else:
        print '[ERROR] ret:%s,cinfo:%s' %(ret,cinfo)
        sys.exit()

    ret,cinfo = DeviceList(vc,SCMD_GET_CONNECTION_INFO_NOW,TGT_DEVICE_DISPLAY_NAME) # cinfo: connection info
    if ret:
        print 'connection type(current): %s' %cinfo
    else:
        print '[ERROR] ret:%s,cinfo:%s' %(ret,cinfo)
        sys.exit()

    nc = None        
    if cinfo == 'Spotify Connect':
        nc = 'Google Cast'
    elif cinfo == 'Google Cast':
        nc = 'Spotify Connect'
    else:
        print '[ERROR] ret:%s,cinfo:%s' %(ret,cinfo)
        sys.exit()

    print 'connection type(to): %s' %nc

    ret,cinfo = DeviceList(vc,SCMD_CHANGE_CONNECTION_TYPE,arg=nc)
    if ret:
        print 'connection type(changed): %s' %cinfo
    else:
        print '[ERROR] ret:%s,cinfo:%s' %(ret,cinfo)
        sys.exit()

    DeviceList(vc,SCMD_SELECT_DEVICE,TGT_DEVICE_DISPLAY_NAME)
    vcsleep(8) # playing stop and go to 'PLAYING FROM .*'

    '''
    print 'press BACK to go "Home"'
    device.press('KEYCODE_BACK')
    vcsleep(5)

    Home(vc,SCMD_PLAYPAUSE) # tap play_btn on 'Home' screen
    vcsleep(10)
    '''
