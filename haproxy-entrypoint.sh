#!/bin/sh
mkdir -p /run/haproxy
chown haproxy:haproxy /run/haproxy
exec haproxy -f /usr/local/etc/haproxy/haproxy.cfg
