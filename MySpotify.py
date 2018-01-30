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
TGT_DEVICE_DISPLAY_NAME = 'HT-Z9F'

execfile('Home.py')
execfile('Playing.py')
execfile('Connecttoadevice.py')
execfile('Settings.py')
execfile('Connecttype.py')

TXT_CTAD = 'Connect to a device'

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
        print k,dict_ids[k]
    return dict_ids

def vcsleep(sec):
    print 'ViwewClient.sleep(%s)' %sec
    ViewClient.sleep(sec)

def tsleep(sec):
    print 'time.sleep(%s)' %sec
    time.sleep(sec)

def debug():
    import pdb; pdb.set_trace()    

# https://qiita.com/everycamel/items/470abe67d83db5140f55
# enum for screen command
(
# HomeMain/Playing
    SCMD_TITLE,
    SCMD_CONNECT,
    SCMD_PLAY,
    SCMD_PLAYPAUSE,
    SCMD_YOUR_LIBRARY_TAB,
    SCMD_SETTINGS,
    SCMD_HOME_TAB,
# Connect to a device
    SCMD_FIND_DEVICE,
    SCMD_SELECT_DEVICE,
    SCMD_OPEN_CONNECTION_TYPE,
    SCMD_GET_CONNECTION_INFO_ALL,
    SCMD_GET_CONNECTION_INFO_NOW,
    SCMD_CHANGE_CONNECTION_TYPE,
# Settings
    SCMD_FIND_SETTING,
    SCMD_SELECT_SETTING
) = range(0,15) # (0,X) X: total number of elements

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

vc       = ViewClient(device, serialno) # vc: ViewClient
uidevice = UiDevice(vc)

# it will fail to set English(United States) "en-rUS" when Language setting is other than "Japanese"
# 
# it will fail to search Language & input when settings in "Japanese"
# languageTo is defined in viewclient.py
# uidevice.changeLanguage(languageTo="en-rUS") # 
# uidevice.openQuickSettingsSettings()

# check android.widget.TextView 
# com.spotify.music:id/glue_toolbar_title : e.g. Home
# com.spotify.music:id/context_title
ret,title = getTitle(vc) # call function defined in Home.py
if ret:
    print 'Now screen title: "%s"' %title
else:
    print 'main screen is not found'
    print 'Is screen locked?'
    sys.exit()

tddn = TGT_DEVICE_DISPLAY_NAME # tddn: target device display name

while True:
    print 'Touch "playPause" to play music,may stop in case playing.'
    Home(vc,SCMD_PLAYPAUSE)
    vcsleep(7)

    print 'Open "Your Library"'
    Home(vc,SCMD_YOUR_LIBRARY_TAB)

    print 'Open "Settings"'
    Home(vc,SCMD_SETTINGS)

    print 'Find "%s" in "Settings" list' %TXT_CTAD
    Settings(vc,SCMD_SELECT_SETTING,TXT_CTAD)

    print 'Open connect type dialog of target device'
    Connecttoadevice(vc,SCMD_OPEN_CONNECTION_TYPE,tddn)

    ret,cinfo = Connecttype(vc,SCMD_GET_CONNECTION_INFO_ALL,tddn) # cinfo: connection info
    if ret:
        print 'Connection type(list)   : %s' %cinfo
    else:
        print '[ERROR] ret:%s,cinfo:%s' %(ret,cinfo)
        sys.exit()

    ret,cinfo = Connecttype(vc,SCMD_GET_CONNECTION_INFO_NOW,tddn) # cinfo: connection info
    if ret:
        print 'Connection type(current): %s' %cinfo
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

    print 'Connection type(to)     : %s' %nc

    ret,cinfo = Connecttype(vc,SCMD_CHANGE_CONNECTION_TYPE,arg=nc)
    if ret:
        print 'Connection type(changed): %s' %cinfo
    else:
        print '[ERROR] ret:%s,cinfo:%s' %(ret,cinfo)
        sys.exit()
    vcsleep(3)

    Connecttoadevice(vc,SCMD_SELECT_DEVICE,tddn)
    vcsleep(7)

    print 'Touch "home_tab" to back "Home"'
    Settings(vc,SCMD_HOME_TAB)
    vcsleep(1)

    print 'Touch "playPause" to play music'
    Home(vc,SCMD_PLAYPAUSE)
    vcsleep(10)
