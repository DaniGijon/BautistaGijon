#!/bin/bash

# vaciar db
$(RM) -r *.out db/
#crear db
mkdir -p db/Registry 

# crear registry 
icegridregistry --Ice.Config=Node.config

#ejecutar downloader
./Downloader.py --Ice.Config=Downloader.config | tee downloader-proxy.out  &

var=$(head -n 1 downloader-proxy.out)

echo "$var"
sleep 1 


#ejecutar orchestrator
./Orchestrator.py --Ice.Config=Orchestrator.config "$var"  | tee orchestrator-proxy.out

var2=$(head -n 1 orchestrator-proxy.out)

echo "$var2"
sleep 1
