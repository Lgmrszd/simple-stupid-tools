#!/usr/bin/env python3
#Simple tool to change text between russian and english keyboard layouts.

import urwid


class Layouts:
    def __init__(self):
        self.layout1 = "ёйцукенгшщзхъ\\фывапролджэячсмитьбю.!\"№;%:?*()_+ЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,"
        self.layout2 = "`qwertyuiop[]\\asdfghjkl;'zxcvbnm,./!@#$%^&*()_+~QWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>?"
        self.layout1_name = "russian"
        self.layout2_name = "english"

    def l1_to_l2(self, s):
       new_s = s
       for i, item in enumerate(s):
           pos = self.layout1.find(item)
           if pos > 0:
               new_s = self.layout2[pos].join([new_s[:i], s[i+1:]])
       return new_s


    def l2_to_l1(self, s):
        new_s = s
        for i, item in enumerate(s):
            pos = self.layout2.find(item)
            if pos > 0:
                new_s = self.layout1[pos].join([new_s[:i], s[i+1:]])
        return new_s


    def swap_l2_l1(self, s):
       new_s = s
       for i, item in enumerate(s):
           pos = self.layout1.find(item)
           if pos > 0:
               new_s = self.layout2[pos].join([new_s[:i], s[i+1:]])
           else:
               pos = self.layout2.find(item)
               if pos > 0:
                   new_s = self.layout1[pos].join([new_s[:i], s[i+1:]])
       return new_s


class TUI:
    def __init__(self):
        self.input_text = urwid.Edit((""), multiline = True)
        self.output_text = urwid.Text("")
        self.button_cyr_to_lat = urwid.Button("Layout 1 to 2")
        self.button_lat_to_cyr = urwid.Button("Layout 2 to 1")
        self.button_swap = urwid.Button("Swap")
        self.button_exit = urwid.Button("Exit")
        self.layouts = Layouts()

    def key(self, input):
        if input in ('q', 'Q'):
            raise urwid.ExitMainLoop()

    def convert(self, edit):
        if edit == self.button_cyr_to_lat:
            self.output_text.set_text(self.layouts.l1_to_l2(self.input_text.get_edit_text()))
        elif edit == self.button_lat_to_cyr:
            self.output_text.set_text(self.layouts.l2_to_l1(self.input_text.get_edit_text()))
        elif edit == self.button_swap:
            self.output_text.set_text(self.layouts.swap_l2_l1(self.input_text.get_edit_text()))
        
    def exit(self, button):
        raise urwid.ExitMainLoop()
    
    def run(self):
        info = urwid.Columns([urwid.Text("Type here:"), urwid.Text("Output:")])
        text_fields = urwid.LineBox(urwid.Columns([self.input_text, 
            ('weight', 0, urwid.SolidFill("|")), self.output_text], box_columns=[1]))
        buttons = urwid.Columns([self.button_lat_to_cyr, self.button_cyr_to_lat,
                 self.button_swap, self.button_exit])
        
        urwid.connect_signal(self.button_cyr_to_lat, 'click', self.convert)
        urwid.connect_signal(self.button_lat_to_cyr, 'click', self.convert)
        urwid.connect_signal(self.button_swap, 'click', self.convert)
        urwid.connect_signal(self.button_exit, 'click', self.exit)
        
        header = urwid.Text("Keyboard layout converter, maybe. " + 
                "Layouts: 1 - " + self.layouts.layout1_name + ", 2 - " + self.layouts.layout2_name)
        items = [header, info, text_fields, buttons]
        listbox = urwid.ListBox(urwid.SimpleListWalker(items))
        loop = urwid.MainLoop(listbox, unhandled_input=self.key)
        loop.run()


if __name__ == '__main__':
    app = TUI()
    app.run()
