import eliza
import dbus, gobject
from dbus.mainloop.glib import DBusGMainLoop


	
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
				talker = eliza.eliza()
				sendmessage( [ purple.PurpleBuddyGetAlias( online ) ] , talker.respond( message ) )
#	print purple.PurpleBuddyGetAlias( account )


bus.add_signal_receiver(my_func,
                        dbus_interface="im.pidgin.purple.PurpleInterface",
                        signal_name="ReceivedImMsg")

loop = gobject.MainLoop()
loop.run()

