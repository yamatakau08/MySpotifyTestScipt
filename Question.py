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

useuiautomatorhelper = True
vc       = ViewClient(device, serialno, useuiautomatorhelper=useuiautomatorhelper) # vc: ViewClient
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
    print 'Screen title: "%s"' %title
else:
    print '[INFO] Screen title is not found'

print 'Touch "home_tab" to back "Home"'
ret = Home(vc,SCMD_HOME_TAB)
if not ret:
    print '[ERROR] Can\'t bak to "Home"!'
    sys.exit()

tddn = TGT_DEVICE_DISPLAY_NAME # tddn: target device display name

print 'Open Playing screen'
Home(vc,SCMD_CONNECT)

print 'Touch "btn_play"'
Playing(vc,SCMD_PLAY)
vcsleep(7)

print 'Touch "btn_play"'
Playing(vc,SCMD_PLAY)
vcsleep(7)

print 'Open "Connect to a device" screen'
Playing(vc,SCMD_CONNECT)

if useuiautomatorhelper:
    vc.uiAutomatorHelper.quit()
