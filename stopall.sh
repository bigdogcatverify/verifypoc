#!/bin/bash

ps -ef | grep python | grep -v grep | awk '{print $2}' | xargs kill

ps -ef | grep npm | grep -v grep | awk '{print $2}' | xargs kill