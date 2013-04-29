import cleverbot
import dbus, gobject
from dbus.mainloop.glib import DBusGMainLoop

import subprocess

def sendnotify(message):
    subprocess.Popen(['notify-send', message])
    return

	
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
bus = dbus.SessionBus()
obj = bus.get_object("im.pidgin.purple.PurpleService", "/im/pidgin/purple/PurpleObject")
purple = dbus.Interface( obj, "im.pidgin.purple.PurpleInterface" )

def sendmessage(group,string):
	for online in purple.PurpleFindBuddies( (purple.PurpleAccountsGetAllActive())[0], '' ):
		if ( purple.PurpleBuddyGetAlias( online ) in group):
			conv = purple.PurpleConversationNew(1, (purple.PurpleAccountsGetAllActive())[ 0 ] , purple.PurpleBuddyGetName( online ) )
			purple.PurpleConvImSend(purple.PurpleConvIm(conv), string)

def my_func(account, sender, message, conversation, flags):
	#print account, "said:", message, sender , conversation
	mail_id = ((str( sender )).split('/'))[ 0 ]
	for online in purple.PurpleFindBuddies( (purple.PurpleAccountsGetAllActive())[0], '' ):
		#print mail_id
		if purple.PurpleBuddyGetName( online ) == mail_id:
				talker = cleverbot.Session()
				sendnotify( "CLBOT : "+str(purple.PurpleBuddyGetAlias( online ))+" has pinged, I will do the talking " )
				
				sendmessage( [ purple.PurpleBuddyGetAlias( online ) ] , talker.Ask( message) )
#	print purple.PurpleBuddyGetAlias( account )


bus.add_signal_receiver(my_func,
                        dbus_interface="im.pidgin.purple.PurpleInterface",
                        signal_name="ReceivedImMsg")

loop = gobject.MainLoop()
loop.run()

