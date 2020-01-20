#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('Trawlnet.ice')
import miModulo
import Example
import IceStorm


class OrchestratorI(miModulo.Orchestrator):
    n=0
    downloader = None
    
    def downloadTask(self,url,current=None):
        print("{0}: {1}".format(self.n, url[0:]))
        sys.stdout.flush()
        self.n += 1
        salida = self.downloader.addDownloadTask(url)
       # salida = (miModulo.FileInfo('miau0','h0'))
        return salida

    def getFileList(self,current=None):
        #lista de canciones
        listaCanciones = (miModulo.FileInfo('s0','h0'),miModulo.FileInfo('s1','h1'),)
        song2 = (miModulo.FileInfo('s2','h2'),)
        listaCanciones = listaCanciones+song2
        
        #song1 = {'name': "nombreSong1", 'hash': "hash1"}
        #song2 = {'name' : 'nombresong2', 'hash' : 'hash2'}
       # listaSongs.append(song2)
        #listaSongs = [("s0","h0")]   
                	        
       # print("{0}: {1}".format(self.n, listaSongs))
       # sys.stdout.flush()
       # self.n += 1
        return listaCanciones

       #nuevo def
    def write(self, message, current=None):
        print("Event received: {0}".format(message))
        sys.stdout.flush()
            
class Orchestrator(Ice.Application):
    #nuevo def: suscriber
    def get_topic_manager(self):
        key = 'IceStorm.TopicManager.Proxy'
        proxy = self.communicator().propertyToProxy(key)
        if proxy is None:
            print("property '{}' not set".format(key))
            return None

        print("Using IceStorm in: '%s'" % key)
        return IceStorm.TopicManagerPrx.checkedCast(proxy)
    
    #nuevo def: publisher
    def get_topic_manager(self):
        key = 'IceStorm.TopicManager.Proxy'
        proxy = self.communicator().propertyToProxy(key)
        if proxy is None:
            print("property {} not set".format(key))
            return None

        print("Using IceStorm in: '%s'" % key)
        return IceStorm.TopicManagerPrx.checkedCast(proxy)

    def run(self, argv):
        
        #nuevo bloque publisher
        topic_mgr = self.get_topic_manager()
        if not topic_mgr:
            print('Invalid proxy')
            return 2

        topic_name = "PrinterTopic"
        try:
            topic = topic_mgr.retrieve(topic_name)
        except IceStorm.NoSuchTopic:
            print("no such topic found, creating")
            topic = topic_mgr.create(topic_name)

        publisher = topic.getPublisher()
        printer = miModulo.OrchestratorPrx.uncheckedCast(publisher)
        #printer = Example.PrinterPrx.uncheckedCast(publisher)

        print("publishing 10 'Hello World' events")
        for i in range(10):
            printer.write("Hello World %s!" % i)
        #hasta aqui


        #nuevo bloque suscriber
        topic_mgr = self.get_topic_manager()
        if not topic_mgr:
            print("Invalid proxy")
            return 2

        ic = self.communicator()
        servant = OrchestratorI()
        adapter = ic.createObjectAdapter("PrinterAdapter")
        subscriber = adapter.addWithUUID(servant)

        topic_name = "PrinterTopic"
        qos = {}
        try:
            topic = topic_mgr.retrieve(topic_name)
        except IceStorm.NoSuchTopic:
            topic = topic_mgr.create(topic_name)

        topic.subscribeAndGetPublisher(qos, subscriber)
        #print(adapter.addWithUUID(servant))
        print("Waiting events... '{}'".format(subscriber))
        #hasta aqui

        
        adapter.activate()
        self.shutdownOnInterrupt()
        ic.waitForShutdown()
        #nuevo linea
        topic.unsubscribe(subscriber)
        
        return 0


sys.exit(Orchestrator().main(sys.argv))
