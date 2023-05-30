# Index - index in bits
# Length - length in bits
# Type - type
headerFields = {
            "fileStamp" : {
                "index": 0,
                "length": 64,
                "type": "str"
            },
            "demoProtocol": {
                "index": 64,
                "length": 8,
                "type": "int"
            },
            "networkProtocol": {
                "index": 96,
                "length": 8,
                "type": "int"
            },
            "serverName": {
                "index": 128,
                "length": 2080,
                "type": "str"
            },
            "clientName": {
                "index": 2208,
                "length": 2080,
                "type": "str"
            },
            "mapName": {
                "index": 4288,
                "length": 2080,
                "type": "str"
            },
            "gameDir": {
                "index": 6368,
                "length": 2080,
                "type": "str"
            },
            "playbackTime": {
                "index": 8448,
                "length": 32,
                "type": "float"
            },
            "playbackTicks": {
                "index": 8480,
                "length": 32,
                "type": "int"
            },
            "playbackFrames": {
                "index": 8512,
                "length": 32,
                "type": "int"
            },
            "signonLength": {
                "index": 8544,
                "length": 32,
                "type": "int"
            }
        }

dataTables = {
     0: "NetNop",
     1: "NetDisconnect",
     2: "NetFile",
     3: "NetTick",
     4: "NetStringCmd",
     5: "NetSetConVar",
     6: "NetSignonState",
     7: "SvcPrint",
     8: "SvcServerInfo",
     9: "SvcSendTable",
    10: "SvcClassInfo",
    11: "SvcSetPause",
    12: "SvcCreateStringTable",
    13: "SvcUpdateStringTable",
    14: "SvcVoiceInit",
    15: "SvcVoiceData",
    17: "SvcSounds",
    18: "SvcSetView",
    19: "SvcFixAngle",
    20: "SvcCrosshairAngle",
    21: "SvcBspDecal",
    23: "SvcUserMessage",
    24: "SvcEntityMessage",
    25: "SvcGameEvent",
    26: "SvcPacketEntities",
    27: "SvcTempEntities",
    28: "SvcPrefetch",
    29: "SvcMenu",
    30: "SvcGameEventList",
    31: "SvcGetCvarValue",
    32: "SvcCmdKeyValues"
}

messageTables = {
    1: "SignOn",
    2: "Packet",
    3: "SyncTick",
    4: "ConsoleCmd",
    5: "UserCmd",
    6: "DataTables",
    7: "Stop",
    8: "StringTables"
}

