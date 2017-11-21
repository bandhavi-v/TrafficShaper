#!/bin/sh
while True; do
	python /home/ats/dialhome.py &
	python /home/ats/main.py &
	python /home/ats/console.py &
	python /home/ats/ifaces_discovery.py &
	sleep(10)
done
