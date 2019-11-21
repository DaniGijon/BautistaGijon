#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('Trawlnet.ice')
import miModulo


class DownloaderI(miModulo.Downloader):
    n = 0

    def addDownloadTask(self, url, current=None):
        print("{0}: {1}".format(self.n, url))
        sys.stdout.flush()
        self.n += 1


class Downloader(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = DownloaderI()

        adapter = broker.createObjectAdapter("DownloaderAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("downloader1"))

        print(proxy, flush=True)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


downloader = Downloader()
sys.exit(downloader.main(sys.argv))