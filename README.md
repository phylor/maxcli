# Maxcli

Maxcli is a command line interface for [MaxSmart](https://www.maxsmart.ch) appliances written in Python.

## Reverse Engineering MaxSmart Power Plugs

Every power plug has an IP address. The power plugs can be discovered using a broadcasted UDP packet. They can be controlled using an HTTP interface exposed on port `80`. The HTTP interface is not secured in any way. The power plugs should therefore not be used in open networks.

### Discovering Power Plugs

The power plugs can be discovered by broadcasting a UDP packet in the network they are connected to. For example:

    echo '00dv=all,2017-10-28,14:09:00,34;' | socat - UDP-DATAGRAM:10.0.255.255:8888,broadcast

Every power plug will respond with another UDP packet, containing its name, serial number and other information about the plug. That UDP packet can be received by the same socket which was used to send the broadcast packet (`socat` shows all received packets on `stdout`). The received UDP packets contain the IP address as a sender.

### Power Plugs' HTTP Interface

It seems that only `GET` requests are required to access and control the power plug. The URL is the IP address of the power plug and supports two parameters, `cmd` and `json`, whereas `cmd` is required and `json` is required depending on the value of `cmd`.

Example:

    curl -D - http://192.168.1.30?cmd=511

Note that the power plug returns an empty response if the request is invalid:

    $ curl -D - http://192.168.1.30?cmd=000
    curl: (52) Empty reply from server

#### Supported `cmd`

Note: not all of these commands are supported by the power plugs. They might only be supported by other products or not supported at all.

| cmd | Description | Required Parameters |
|-----|-------------|---------------------|
| 001 | sets wifi | `mode`, `ssid`, `password`, `security` |
| 002 | gets signal? | |
| 046 | radio? | `sn` |
| 111 | registers device? connects to `slave_url` | `sn`, `sak` |
| 112 | delete a device? | `sn`, `sak` |
| 114 | repeater button? | `sn`, `repeater` |
| 120 | sets an `op` to 1 or 2, 2 == restore? also hints for reboot | |
| 200 | switches the relay inside the power plug | `sn`, `port`, `state` |
| 201 | sets the name | `sn`, `port`, `name` |
| 202 | sets master and limit | `sn`, `master`, `limit` |
| 204 | sets a timer | `sn`, `port`, `start`, `delay` |
| 205 | sets cost and money | `sn`, `cost`, `money` |
| 206 | sets a rule | `sn`, `rule [ en, port, time, day, rname ]` |
| 207 | sets data? | `senddata` |
| 230 | sets a rule | `sn`, `rule [ en, trig [ id, cond, data ], tagsn, port, delay, op, spk, day, time ]` |
| 231 | sets a name? | `sn`, `id`, `sname` |
| 250 | | `sn`, `mode`, `ledid`, `r`, `g`, `b`, `br` |
| 251 | sets a rule | `sn`, `rule [ rname, en, time, spk, day, r, g, b, br ]` |
| 253 | plays music (control == 0 replays, control == 2 pauses) | `type`, `control`, `url` |
| 500 | `slave_url`? | `dev` |
| 502 | returns the current time | `sn` |
| 510 | returns the watt history | `sn`, `type` |
| 511 | returns current watt and amp, and whether the relay is on or off | `sn` |
| 512 | returns master and limit | |
| 515 | returns the timer | `sn`, `port` |
| 516 | returns the rule list | `sn`, `page` |
| 517 | returns a rule? anti burglar? | `sn` |
| 520 | returns a repeater? | `sn` |
| 530 | returns sensor rule? | `sn` |
| 531 | | `sn` |
| 532 | login? | `sn`, `id`, `type` |
| 551 | returns state of music? | `sn` |
| 552 | returns all rules? | `sn` |
