#!/bin/bash

grep "$1" doors.data.txt | awk '{print $3" "$4}'
grep "$2" doors.data.txt | awk '{print $3" "$4}'
