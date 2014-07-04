#!/usr/bin/python
# -*- coding: cp1251 -*-

# timeworker.py


import wx
import wx.html as html
import twdb
import datetime

ID_CLOSE = 1
ID_INOUT = 2
ID_REFR = 3

page = '<html><body bgcolor="#8e8e95"> \
<b>TimeWorker</b><hr>\
Uses mongoDB (pymongo lib) for database control<br>\
Uses wxPython for GUI<br><hr>\
Press [Arr/Dep] button to check-in or check-out<br>\
</body></html>'


class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(400, 290))

        panel = wx.Panel(self, -1)

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.htmlwin = html.HtmlWindow(panel, -1, style=wx.NO_BORDER)
        self.htmlwin.SetBackgroundColour(wx.RED)
        self.htmlwin.SetStandardFonts()
        self.htmlwin.SetPage(page)

        vbox.Add((-1, 10), 0)
        vbox.Add(self.htmlwin, 1, wx.EXPAND | wx.ALL, 9)


        buttonOk = wx.Button(panel, ID_CLOSE, 'Ok')
        buttonInOut = wx.Button(panel, ID_INOUT, 'Arr/Dep')
        buttonRefresh = wx.Button(panel, ID_REFR, 'Refresh')

        self.Bind(wx.EVT_BUTTON, self.OnClose, id=ID_CLOSE)
        self.Bind(wx.EVT_BUTTON, self.GetToday, id=ID_INOUT)
        self.Bind(wx.EVT_BUTTON, self.OnRefresh, id=ID_REFR)

        hbox.Add((100, -1), 1, wx.EXPAND | wx.ALIGN_RIGHT)
        hbox.Add(buttonRefresh, flag=wx.TOP | wx.BOTTOM | wx.RIGHT, border=10)
        hbox.Add(buttonInOut, flag=wx.TOP | wx.BOTTOM | wx.RIGHT, border=10)
        hbox.Add(buttonOk, flag=wx.TOP | wx.BOTTOM | wx.RIGHT, border=10)
        vbox.Add(hbox, 0, wx.EXPAND)

        panel.SetSizer(vbox)
        self.Centre()
        self.Show(True)

    def OnClose(self, event):
        self.Close()

    def OnRefresh(self, event):
        self.htmlwin.SetPage(twdb.generatePage(''))

    def GetToday(self, event):
        page = twdb.whatAboutToday(datetime.datetime.today(), \
                                   'localhost', 27017, 'timeworker')
        self.htmlwin.SetPage(page)

app = wx.App(0)
MyFrame(None, -1, 'TimeWorker')
app.MainLoop()
