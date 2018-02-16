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

execfile('common_lib.py')
execfile('Home.py')
execfile('Playing.py')
execfile('Connecttoadevice.py')
execfile('Settings.py')
execfile('Connecttype.py')

TXT_CTAD = 'Connect to a device'

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
    SCMD_DEVICE,
    SCMD_OPEN_CONNECTION_TYPE,
    SCMD_GET_CONNECTION_INFO_ALL,
    SCMD_GET_CONNECTION_INFO_NOW,
    SCMD_CHANGE_CONNECTION_TYPE,
# Settings
    SCMD_SETTING,
) = range(0,13) # (0,X) X: total number of elements

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

useuiautomatorhelper = False
vc       = ViewClient(device, serialno,useuiautomatorhelper=useuiautomatorhelper) # vc: ViewClient
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
if useuiautomatorhelper:
    vcsleep(2) # workarround to avoid "WARNING: xxx not found. Perhaps the device has hardware buttons. "

ret,title = getTitle(vc) # call function defined in Home.py
if ret:
    print 'Screen title: "%s"' %title
else:
    print '[INFO] Screen title is not found'

print 'Touch "home_tab" to back "Home"'
ret = Home(vc,SCMD_HOME_TAB,VOP_TOUCH)
if not ret:
    print '[ERROR] Can\'t bak to "Home"!'
    sys.exit()

tddn = TGT_DEVICE_DISPLAY_NAME # tddn: target device display name

while True:
    print 'Touch "playPause" to play music,may stop in case playing.'
    ret = Home(vc,SCMD_PLAYPAUSE,VOP_TOUCH)
    if not ret:
        sys.exit()

    vcsleep(7)

    print 'Open "Your Library"'
    Home(vc,SCMD_YOUR_LIBRARY_TAB,VOP_TOUCH)

    vcsleep(5)
    print 'Open "Settings"'
    Home(vc,SCMD_SETTINGS,VOP_TOUCH)

    print 'Find "%s" in "Settings" list' %TXT_CTAD

    # Spotify App Version 8.4.39.673 armV7 on Xperia Z3
    # Since it's a little bit hard to find text "Connect to a device" item,use text 'Listen to and control Spotify on your devices.' instead
    #txt = TXT_CTAD    
    txt = 'Listen to and control Spotify on your devices.'
    Settings(vc,SCMD_SETTING,VOP_TOUCH,txt)

    print 'Open connection type dialog of target device'
    ret = Connecttoadevice(vc,SCMD_OPEN_CONNECTION_TYPE,VOP_TOUCH,tddn)
    if not ret:
        print '[ERROR] Can\'t open connection type dialog!'
        sys.exit()

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
    elif cinfo == 'Forget this device':
        nc = cinfo
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

    Connecttoadevice(vc,SCMD_DEVICE,VOP_TOUCH,tddn)
    vcsleep(7)

    print 'Touch "home_tab" to back "Home"'
    Settings(vc,SCMD_HOME_TAB,VOP_TOUCH)
    vcsleep(1)

    print 'Touch "playPause" to play music'
    Home(vc,SCMD_PLAYPAUSE,VOP_TOUCH)
    vcsleep(10)
