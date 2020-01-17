#!/usr/bin/make -f
# -*- mode:makefile -*-

all:

clean:
	$(RM) -r *.out db/

run-registry:
	mkdir -p db/Registry 
	icegridregistry --Ice.Config=Node.config

run-downloader:
	./Downloader.py --Ice.Config=Downloader.config | tee downloader-proxy.out

run-orchestrator:
	./Orchestrator.py --Ice.Config=Orchestrator.config '$(shell head -1 downloader-proxy.out)' 'DaniGijon' | tee orchestrator-proxy.out

run-orch:
	./Orchestrator.py --Ice.Config=Orchestrator.config | tee orchestrator-proxy.out
	
run-cliente:
	./Cliente.py --Ice.Config=Cliente.config '$(shell head -1 orchestrator-proxy.out)' 'https://www.youtube.com/watch?v=1V_xRb0x9aw' 'download'