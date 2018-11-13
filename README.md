# RouterConfig

### How to use it?
1. Place 'RouterConfig' under '/'.
2. Create a log directory: /var/log/RouterConfig.
3. Install related dependencies.
   pip install -r /RouterConfig/requirements.txt
4. Configure the software to boot from the boot.(optional)
   1) Add the following to the /etc/rc.loacl file: sudo python /RouterConfig/RouterConfig/main.py &

### Configuration file:

The file should be placed under `/root`, and should be named as `config.json`.

```json
{
    "route_config": {
        "bgp": {
            "as_num": as号,
            "network": ["直连网络号"],
            "ebgp_neighbors": [
                {
                    "neighbor_ip": "ebgp邻居IP地址",
                    "neighbor_as": ebgp邻居as号
                }
            ],
            "ibgp_neighbors": ["ibgp邻居IP地址"],
            "others": ["其他bgp配置命令"]
        },
        "ospf": {
            "networks": [
                {
                    "network": "直连网络号",
                    "area": 所属ospf区域
                }
            ],
            "others": ["其他ospf配置命令"]
        },
        "static": [
            {
                "next_hop": "出接口或下一跳ip地址",
                "dst_prefix": "目标网段"
            }
        ],
        "rip": {
            "version": rip的版本号(1或2),
            "networks": ["直连网络号"],
            "others": ["其他rip配置命令"]
        }
    },
    "data_filter": [
        {
            "source_mac": "根据源mac进行过滤",
            "ip_address": {
                "src": ["根据源ip地址进行过滤"],
                "dst": ["根据目的ip地址进行过滤"]
            },
            "port": {
                "src": ["根据四层源端口进行过滤"],
                "dst": ["根据四层目的端口进行过滤"]
            },
            "protocol": "需要过滤的协议，包括all、tcp、udp、icmp，默认是all",
            "nic": {
                "in": "根据入网卡名进行过滤",
                "out": "根据出网卡名进行过滤"
            }
        }
    ],
    "congestion_control": [
        {
            "nic": "网卡名",
            "speed": "设置的端口带宽(单位包括bit,kbit,mbit,gbit,tbit,bps,kbps,mbps,gbps,tbps)"
        }
    ],
    "priority_stategy": [
        {
            "source_mac": "根据源mac进行匹配",
            "ip_address": {
                "src": ["根据源ip地址进行匹配"],
                "dst": ["根据目的ip地址进行匹配"]
            },
            "port": {
                "src": ["根据四层源端口进行匹配"],
                "dst": ["根据四层目的端口进行匹配"]
            },
            "protocol": "需要过滤的协议，包括all、tcp、udp、icmp，默认是all",
            "interface": "优先级队列所在的网卡名",
            "priority": "需要设置的优先级，包括low、normal、high，默认都是normal"
        }
    ]
}
```   

> - `source_mac` and `out` in `nic` cannot coexist!
> - If you want to specify `port`, you must specify `protocol`, and its value cannot be 'all', it must be specific to 'udp' or 'tcp'.
> - If you do not specify `ip_address`, all ip addresses are filtered by default.
> - If you do not specify `protocol`, all types of data are filtered by default.
> - All of the above can be unspecified, and all traffic is filtered by default.

### Configuration file example:

```json
{
    "route_config": {
        "bgp":
        {
            "as_num": 100,
            "network": ["2.0.0.0/24"],
            "ebgp_neighbors":
            [
                {
                    "neighbor_ip": "2.0.0.44",
                    "neighbor_as": 101
                }
            ],
            "ibgp_neighbors":[],
            "others":[]
        },
        "ospf": {},
        "rip": {
            "version": 1,
            "networks": ["1.0.0.0/24", "2.0.0.0/24"],
            "others": []
        },
        "static": [
            {
                "next_hop": "2.0.0.1",
                "dst_prefix": ["100.0.0.0/24", "101.0.0.0/24"]
            },
            {
                "next_hop": "eth0",
                "dst_prefix": ["102.0.0.0/24"]
            }
        ]
    },
    "data_filter": [
        {
            "source_mac": "00:00:00:00:00:01",		
            "ip_address": {
                "src": ["1.0.0.1", "2.0.0.1"],
                "dst": ["3.0.0.1"]
            },
            "port": {
                "src": "80",
                "dst": "80"
            },
            "protocol": "all",
            "nic": {
                "in": "eth0",
                "out": "eth1"
            }
        },
        {
            "ip_address": {
                "dst": ["3.0.0.1"]
            },
            "port": {
                "src": "80"
            },
            "protocol": "tcp"
        }
    ],
    "congestion_control": [
        {
            "nic": "eth0",
            "speed": "100mbit"
        },
        {
            "nic": "eth1",
            "speed": "10bps"
        }
    ],
    "priority_strategy": [
        {
            "source_mac": "00:00:00:00:00:02",
            "ip_address": {
                "src": ["1.0.0.1", "2.0.0.1"],
                "dst": ["3.0.0.1"]
            },
            "port": {
                "src": "80",
                "dst": "80"
            },
            "protocol": "tcp",
            "interface": "eth0",
            "priority": "high"
        }
    ]
}
```
