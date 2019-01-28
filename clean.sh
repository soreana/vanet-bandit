#!/usr/bin/env bash

sudo mn -c && sudo netstat -nlp | grep 6653 |awk '{print $7}' | sed -e 's,[[:alpha:]],,g' | sed -e 's,\/,,g' | xargs sudo kill -9

