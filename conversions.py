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

chamberNames = {
    "testchmb_a_00": "00/01",
    "testchmb_a_01": "02/03",
    "testchmb_a_02": "04/05", 
    "testchmb_a_03": "06/07",
    "testchmb_a_04": "08",
    "testchmb_a_05": "09",
    "testchmb_a_06": "10",
    "testchmb_a_07": "11/12",
    "testchmb_a_08": "13",
    "testchmb_a_08_advanced": "13 Advanced",
    "testchmb_a_09": "14",
    "testchmb_a_09_advanced": "14 Advanced",
    "testchmb_a_10": "15",
    "testchmb_a_10_advanced": "15 Advanced",
    "testchmb_a_11": "16",
    "testchmb_a_11_advanced": "16 Advanced",
    "testchmb_a_13": "17",
    "testchmb_a_13_advanced": "17 Advanced",
    "testchmb_a_14": "18",
    "testchmb_a_14_advanced": "18 Advanced",
    "testchmb_a_15": "19",
    "escape_00": "Escape 00",
    "escape_01": "Escape 01",
    "escape_02": "Escape 02"
}