@echo off

REM Replace <subreddit_name> with the subreddit you want to monitor
set SUBREDDIT_NAME=<subreddit_name>

python EvmosRosetta.py --subreddit %SUBREDDIT_NAME%
