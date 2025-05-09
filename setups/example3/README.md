# Example 3: Real Hardware

## Overview

### What is this experiment doing?
The testbed is subdivided in two area, each area consists of a network bridge, two Instances and a subnet. Each of the network bridges is connected to a physical port of the testbed host.

Between these physical ports (and therefore both subnets) a hardware router is routing, in our testcase another Linux machine is used.

During the experiments, Integrations will switch the port speed of eno2 and eno3 to 100Mbit/s without auto-negotiation to test how the router reacts to such scenarios, and what kind of implication its reaction to the Applications has.

This example shows the possibility to integrate real hardware to a testbed and use the testbed system to conduct real end-to-end tests with application workloads over physical hardware. 

Example results can be found at `results/example3`.

### Schematic testbed overview
```
+---------------+                                        +---------------+
|  a1-endpoint  |      +---------------------------+     |  b1-endpoint  |
|               |      |      HARDWARE ROUTER      |     |               |
| Apps:         |      |        10.0.1.1/24        |     | Apps:         |
| iperf-server  |      |        10.0.2.1/24        |     | iperf-client  |
|               |      +---------------------------+     | ping          |
|  10.0.1.2/24  |        ||                    ||        |  10.0.2.2/24  |
+---------------+        ||                    ||        +---------------+
|     eth1      |====\\  OO eno2          eno3 OO  //====|     eth1      |
+---------------+    ||  ||                    ||  ||    +---------------+
+---------------+    ||  ||      Physical      ||  ||    +---------------+
|  a2-endpoint  |    ||  ||       Ports        ||  ||    |  b2-endpoint  |
|               |  +--------+                +--------+  |               |
| Apps:         |  | Bridge |                | Bridge |  | Apps:         |
| iperf-server  |  | exp0   |                | exp1   |  | iperf-client  |
| ping          |  +--------+                +--------+  |               |
|  10.0.1.3/24  |    ||                            ||    |  10.0.2.3/24  |
+---------------+    ||                            ||    +---------------+
|     eth1      |====//                            \\====|     eth1      |
+---------------+                                        +---------------+
```

## Guide

**Please Note:** It is assumed, that `eno2` and `eno3` are the physical interfaces of the Testbed Hosts for this experiment. If the names differ in your setup, change the interfaces in `testbed.json` accordingly.

0. Create a base image as described in `/baseimage_creation/README.md`. Start a session as `root` user.


1. Build current version of Instance Manager:
   ```bash
   cd <proto-testbed>/instance-manager/
   make all
   ```

2. Prepare the VM image (if the Instance Manager was not installed before):
    ```bash
    cd <proto-testbed>/baseimage-creation
    ./im-installer.py -i <path/to/your/baseimage> -o /tmp/endpoint.qcow2 -p ../instance-manager/instance-manager.deb
    ```

3. Install ethtool on the Testbed Host
   ```bash
    apt install -y ethtool
   ```

3. Load required environment variable (select an experiment tag):
    ```bash
    export EXPERIMENT_TAG=hardware_test
    ```

4. Start the testbed:
   ```bash
   cd proto-testbed
   ./proto-testbed -e $EXPERIMENT_TAG setups/example3
   ```

5. Export the results (and clean up):
   ```bash
   ./proto-testbed export -e $EXPERIMENT_TAG -o ./${EXPERIMENT_TAG}-images image setups/example1
   ./proto-testbed export -e $EXPERIMENT_TAG -o ./${EXPERIMENT_TAG}-csvs csv setups/example1 

    # Optional: Clean up data from InfluxDB (Should be done before repeating the experiment)
   ./proto-testbed clean -e $EXPERIMENT_TAG

    # Optional: Delete disk images (After all experiments are completed)
    rm /tmp/endpoint.qcow2
   ```

## Set up a Linux host as router
The host has the interfaces `eno2` (connected to `eno2` of the Testbed Host) and `eno3` (connected to `eno3` of the Testbed Host):
```bash
sudo -s
sysctl -w net.ipv4.ip_forward=1
iptables --policy FORWARD ACCEPT

ip address add 10.0.1.1/24 dev eno2
ip address add 10.0.2.1/24 dev eno3

ip link set up dev eno2
ip link set up dev eno3
```
