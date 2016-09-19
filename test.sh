#!/bin/bash

SERVICE="localhost:5000"
OPTIONS=-v

http $OPTIONS GET "$SERVICE/"

http $OPTIONS DELETE "$SERVICE/user/"

http $OPTIONS POST "$SERVICE/user/?x=1000&y=3&name=Mark&age=30"
http $OPTIONS POST "$SERVICE/user/?x=2000&y=3&name=Victor&age=33"
http $OPTIONS POST "$SERVICE/user/?x=3000&y=3&name=Mary&age=35"
http $OPTIONS POST "$SERVICE/user/?x=4000&y=3&name=Elena&age=36"
http $OPTIONS POST "$SERVICE/user/?x=5000&y=3&name=Sam&age=37"

# Two users should be returned
http $OPTIONS GET "$SERVICE/user/0/neighbors?k=2&radius=10000"
# Two users should be returned
http $OPTIONS GET "$SERVICE/user/0/neighbors?k=10&radius=2500"

http $OPTIONS DELETE "$SERVICE/user/4"
http $OPTIONS DELETE "$SERVICE/user/4"

http $OPTIONS GET "$SERVICE/user/1"
http $OPTIONS PUT "$SERVICE/user/1?x=7000&y=3&name=Brad&age=10"
http $OPTIONS GET "$SERVICE/user/1"

http $OPTIONS POST "$SERVICE/generate?n=1000"
http $OPTIONS GET "$SERVICE/user/0/neighbors?k=2&radius=5000"
