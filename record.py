# examples/record_demo.py -- demonstrate record extension
#
#    Copyright (C) 2006 Alex Badea <vamposdecampos@gmail.com>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA



# Change path so we find Xlib
# sys.path.insert(1, os.path.join(sys.path[0], '..')) # Was in the example code, but seems to be uneeded

from Xlib import X, XK, display
from Xlib.ext import record
from Xlib.protocol import rq

class Record():

    def __init__(self):
        self.local_dpy = display.Display()
        self.record_dpy = display.Display()
        self.ctrlDown = False
        self.altDown = False
        self.delDown = False
        self.shiftDown = False
        self.escDown = False
        # Check if the extension is present
        if not self.record_dpy.has_extension("RECORD"):
            print("RECORD extension not found")
            sys.exit(1)
        self.r = self.record_dpy.record_get_version(0, 0)
        # print("RECORD extension version %d.%d" % (r.major_version, r.minor_version)) # Spam

        # Create a recording context; we only want key and mouse events
        self.ctx = self.record_dpy.record_create_context(
                0,
                [record.AllClients],
                [{
                        'core_requests': (0, 0),
                        'core_replies': (0, 0),
                        'ext_requests': (0, 0, 0, 0),
                        'ext_replies': (0, 0, 0, 0),
                        'delivered_events': (0, 0),
                        'device_events': (X.KeyPress, X.MotionNotify),
                        'errors': (0, 0),
                        'client_started': False,
                        'client_died': False,
                }])

    def lookup_keysym(self,keysym):
        for name in dir(XK):
            if name[:3] == "XK_" and getattr(XK, name) == keysym:
                return name[3:]
        return "[%d]" % keysym

    def record_callback(self,reply):
        if reply.category != record.FromServer:
            return
        if reply.client_swapped:
            print("* received swapped protocol data, cowardly ignored")
            return
        if not len(reply.data) or reply.data[0] < 2:
            # not an event
            return

        data = reply.data
        while len(data):
            event, data = rq.EventField(None).parse_binary_value(data, self.record_dpy.display, None, None)

            if event.type in [X.KeyPress, X.KeyRelease]:
                pr = event.type == X.KeyPress and "Press" or "Release"

                keysym = self.local_dpy.keycode_to_keysym(event.detail, 0)
                if not keysym:
                    print("KeyCode %s %s" % (pr, event.detail))
                else:
                    key = self.lookup_keysym(keysym)
                    print("KeyStr %s %s" % (pr, key))
                    if keysym == XK.XK_Alt_L or keysym == XK.XK_Alt_R:
                        if event.type == X.KeyPress:
                            self.altDown = True
                        else:
                            self.altDown = False
                    elif keysym == XK.XK_Control_L or keysym == XK.XK_Control_R:
                        if pr == "Press":
                            self.ctrlDown = True
                        else:
                            self.ctrlDown = False
                    elif keysym == XK.XK_Delete:
                        if pr == "Press":
                            self.delDown = True
                        else:
                            self.delDown = False
                    elif keysym == XK.XK_Escape:
                        if pr == "Press":
                            self.escDown = True
                        else:
                            self.escDown = False
                    elif keysym == XK.XK_Shift_L or keysym == XK.XK_Shift_R:
                        if pr == "Press":
                            self.shiftDown = True
                        else:
                            self.shiftDown = False
            if (self.ctrlDown and self.altDown and self.delDown) or (self.ctrlDown and self.shiftDown and self.escDown):
                # Send a signal for the main thread to show the main window and start scanning
                print("works")

                # For reference, this stops the loop once Escape is pressed
                # if event.type == X.KeyPress and keysym == XK.XK_Escape:
                #     local_dpy.record_disable_context(ctx)
                #     local_dpy.flush()
                #     return


