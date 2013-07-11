#!/usr/bin/python
# -*- coding: UTF-8 -*-

import datetime
import threading

import wx

from outwiker.core.commands import getCurrentVersion, MessageBox, setStatusText
from outwiker.core.version import Version

from .i18n import get_
from .longprocessrunner import LongProcessRunner
from .updatedialog import UpdateDialog
from .updatesconfig import UpdatesConfig
from .versionlist import VersionList

# Событие срабатывает, когда завершается "молчаливое" обновление списка версий
# Параметр verList - экземпляр класса VersionList
UpdateVersionsEvent, EVT_UPDATE_VERSIONS = wx.lib.newevent.NewEvent()


class UpdateDialogController (object):
    """
    Контроллер для управления UpdateDialog.
    Сюда вынесена вся логика.
    """
    def __init__ (self, application):
        global _
        _ = get_()

        self._application = application

        # Экземпляр потока, который будет проверять новые версии
        self._silenceThread = None
        self._application.mainWindow.Bind (EVT_UPDATE_VERSIONS, handler=self._onVersionUpdate)


    def _prepareUpdates (self, verList, updateDialog):
        """
        Сверяем полученные номера версий с теми, что установлены сейчас и заполняем диалог изменениями (updateDialog)
        Возвращает True, если есть какие-нибудь обновления
        """
        currentVersion = getCurrentVersion()
        stableVersion = verList.getStableVersion()
        unstableVersion = verList.getUnstableVersion()

        # Есть ли какие-нибудь обновления?
        hasUpdates = False

        updateDialog.setCurrentOutWikerVersion (currentVersion)

        if stableVersion != None:
            hasUpdates = hasUpdates or (currentVersion < stableVersion)
            updateDialog.setLatestStableOutwikerVersion (stableVersion, currentVersion < stableVersion)
        else:
            updateDialog.setLatestStableOutwikerVersion (currentVersion, False)

        if unstableVersion != None:
            hasUpdates = hasUpdates or (currentVersion < unstableVersion)
            updateDialog.setLatestUnstableOutwikerVersion (unstableVersion, currentVersion < unstableVersion)
        else:
            updateDialog.setLatestUnstableOutwikerVersion (currentVersion, False)

        for plugin in self._application.plugins:
            pluginVersion = verList.getPluginVersion (plugin.name)

            try:
                currentPluginVersion = Version.parse (plugin.version)
            except ValueError:
                continue

            try:
                pluginUrl = verList.getPluginUrl (plugin.name)
            except KeyError:
                continue

            if (pluginVersion != None and
                    pluginVersion > currentPluginVersion):
                updateDialog.addPluginInfo (plugin,
                        pluginVersion,
                        verList.getPluginUrl (plugin.name))
                hasUpdates = True

        UpdatesConfig (self._application.config).lastUpdate = datetime.datetime.today()
        return hasUpdates


    def ShowModal (self):
        """
        Проверить обновления и показать диалог с результатами
        """
        verList = VersionList (self._application.plugins)

        progressRunner = LongProcessRunner (verList.updateVersions, 
                self._application.mainWindow,
                dialogTitle = u"UpdateNotifier",
                dialogText = _(u"Check for new versions..."))

        progressRunner.run()

        updateDialog = UpdateDialog (self._application.mainWindow)
        hasUpdates = self._prepareUpdates (verList, updateDialog)

        if hasUpdates:
            updateDialog.ShowModal()
        else:
            MessageBox (_(u"Updates not found"),
                    u"UpdateNotifier")
        updateDialog.Destroy()


    def _onVersionUpdate (self, event):
        setStatusText (u"")
        updateDialog = UpdateDialog (self._application.mainWindow)
        hasUpdates = self._prepareUpdates (event.verList, updateDialog)

        if hasUpdates:
            updateDialog.ShowModal()
        updateDialog.Destroy()
        self._silenceThread = None


    def _silenceThreadFunc (self, verList):
        """
        Функция потока для молчаливой проверки обновлений
        """
        verList.updateVersions()
        event = UpdateVersionsEvent (verList=verList)

        if self._application.mainWindow:
            wx.PostEvent (self._application.mainWindow, event)

            
    def updateSilence (self):
        """
        Молчаливое обновление списка версий
        """
        setStatusText (_(u"Check for new versions..."))
        verList = VersionList (self._application.plugins)

        if (self._silenceThread == None or
                not self._silenceThread.isAlive()):

            self._silenceThread = threading.Thread (None, self._silenceThreadFunc, args=(verList,))
            self._silenceThread.start()