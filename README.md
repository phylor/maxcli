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

| cmd | Description | Required Parameters |
|-----|-------------|---------------------|
| 046 | | |
| 111 | | |
| 112 | | |
| 114 | | |
| 120 | sets an `op` to 1 or 2 | |
| 200 | switches the relay inside the power plug | |
| 201 | sets the name | |
| 204 | sets a timer | |
| 205 | sets cost and money | |
| 206 | | |
| 502 | returns the current time | |
| 510 | returns the watt history | |
| 511 | returns current watt and amp, and whether the relay is on or off | |
| 512 | returns master and limit | |
| 515 | returns the timer | |
| 517 | returns a rule? | |
| 520 | | |
| 531 | | |
| 552 | returns all rules? | |
