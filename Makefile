all:

depend:
	python3 -m pip install -U aiohttp
	python3 -m pip install -U ipaddress

.PHONY: all  depend
