@echo off
cd "../astron/"
title Toontown Infinite Astron

:start
astrond --loglevel info config/cluster.yml
PAUSE
goto start