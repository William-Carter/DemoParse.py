import bitstring
import conversions
import levelSplits
import neatTables

class Message:
    def __init__(self, type: str, offset: int, stream: bitstring.BitStream, bits_overheadSize: int):
        self.type = type
        self.stream = stream
        self.offset = offset
        self.tick = stream[offset+8:offset+40].intle
        self.bits_overheadSize = bits_overheadSize
    
    def parse(self):
        raise "Type-specific message class must be used when parsing messages!"
        

class PacketMessage(Message):
    def __init__(self, offset: int, stream: bitstring.BitStream):
        super().__init__("Packet", offset, stream, 93*8)
        self.parse()
        self.bits_size = self.bits_overheadSize+self.bits_dataSize

    def parse(self):
        localOffset = self.offset+5*8
        self.flags = self.stream[localOffset:localOffset+4*8]
        localOffset += 4*8
        self.viewOrigin = []
        for i in range(3):
            self.viewOrigin.append(self.stream[localOffset:localOffset+4*8].floatle)
            localOffset += 4*8

        self.viewAngles = []
        for i in range(3):
            self.viewAngles.append(self.stream[localOffset:localOffset+4*8].floatle)
            localOffset += 4*8

        self.localViewAngles = []
        for i in range(3):
            self.localViewAngles.append(self.stream[localOffset:localOffset+4*8].floatle)
            localOffset += 4*8


        self.viewOrigin2 = []
        for i in range(3):
            self.viewOrigin2.append(self.stream[localOffset:localOffset+4*8].floatle)
            localOffset += 4*8

        self.viewAngles2 = []
        for i in range(3):
            self.viewAngles2.append(self.stream[localOffset:localOffset+4*8].floatle)
            localOffset += 4*8

        self.localViewAngles2 = []
        for i in range(3):
            self.localViewAngles2.append(self.stream[localOffset:localOffset+4*8].floatle)
            localOffset += 4*8

        self.inSequence = self.stream[localOffset:localOffset+4*8].intle
        localOffset += 4*8
        self.outSequence = self.stream[localOffset:localOffset+4*8].intle
        localOffset += 4*8

        self.bits_dataSize = self.stream[localOffset:localOffset+4*8].intle*8
        
class ConsoleCommandMessage(Message):
    def __init__(self, offset: int, stream: bitstring.BitStream):
        super().__init__("ConsoleCmd", offset, stream, 9*8)
        self.parse()
        self.bits_size = self.bits_overheadSize+self.bits_dataSize

    def parse(self):
        self.bits_dataSize = self.stream[self.offset+5*8:self.offset+9*8].intle*8
        self.data = self.stream[self.offset+9*8:self.offset+(9*8)+self.bits_dataSize].bytes
        
class DataTablesMessage(Message):
    def __init__(self, offset: int, stream: bitstring.BitStream):
        super().__init__("DataTables", offset, stream, 9*8)
        self.parse()
        self.bits_size = self.bits_overheadSize + self.bits_dataSize

    def parse(self):
        self.bits_dataSize = self.stream[self.offset+5*8:self.offset+9*8].intle*8
        
class SyncTickMessage(Message):
    def __init__(self, offset: int, stream: bitstring.BitStream):
        super().__init__("SyncTick", offset, stream, 5*8)
        self.parse()
        self.bits_size = self.bits_overheadSize+self.bits_dataSize

    def parse(self):
        self.bits_dataSize = 0
        
class UserCommandMessage(Message):
    def __init__(self, offset: int, stream: bitstring.BitStream):
        super().__init__("UserCmd", offset, stream, 13*8)
        self.parse()
        self.bits_size = self.bits_overheadSize + self.bits_dataSize

    def parse(self):
        self.bits_dataSize = self.stream[self.offset+9*8:self.offset+13*8].intle*8

class StringTablesMessage(Message):
    def __init__(self, offset: int, stream: bitstring.BitStream):
        super().__init__("StringTables", offset, stream, 9*8)
        self.parse()
        self.bits_size = self.bits_overheadSize+self.bits_dataSize

    def parse(self):
        self.bits_dataSize = self.stream[self.offset+5*8:self.offset+9*8].intle*8

class DemoParse:
    def __init__(self, filePath, offset=0):
        with open(filePath, 'rb') as f:
            stream = bitstring.BitStream(bytes=f.read())
        
        # Get demo header
        self.headerFieldValues = {}

        for field in conversions.headerFields.keys():
            self.headerFieldValues[field] = self.pullField(conversions.headerFields[field], stream)

        fileSize = len(stream)
        currentOffset = 1072*8 # The end of the header/start of the data (in bits)
        self.demoLength = int(round(offset/0.015, 0))
        
        self.autoStarted = None
        self.autoEnded = None
        
        splitBounds = levelSplits.splits[self.headerFieldValues["mapName"]].copy()
        self.splits = []
        lastTickAngle = None
        while True:
            
            # End loop if we've reached the end of the file
            if currentOffset >= fileSize:
                break
            parsedMessage = self.parseMessage(currentOffset, stream)
            
            if not parsedMessage:
                break
            else:
                if parsedMessage.type == "ConsoleCmd":
                    if parsedMessage.data.decode("utf-8").rstrip('\x00') == "startneurotoxins 99999":
                        self.autoEnded = self.demoLength + 1# idk why adding one is necessary but it is

                if parsedMessage.type == "UserCmd":
                    
                    self.demoLength += 1


                if parsedMessage.type == "Packet":
                    
                    for split in splitBounds:
                        if levelSplits.checkInside(parsedMessage.viewOrigin, split["bounds"]):
                            
                            effectiveDemoLength = self.demoLength
                            if self.autoStarted:
                                effectiveDemoLength -= self.autoStarted
                            
                            self.splits.append((split["name"], effectiveDemoLength))
                            splitBounds.remove(split)
                    
                    if self.autoStarted == None:
                        if not lastTickAngle == None:
                            if parsedMessage.viewAngles != lastTickAngle and lastTickAngle != [0.0, 0.0, 0.0]:
                                # Technically this could cause issues but i'm sure it's fiiiiiiine
                                if round(parsedMessage.viewAngles[1], 6)  == -170.002441:
                                    self.autoStarted = self.demoLength+1
                                    
                                
                    

                    lastTickAngle = parsedMessage.viewAngles

                        
                currentOffset += parsedMessage.bits_size

        self.demoLength += 1 # 0th tick xD
        effectiveDemoLength = self.demoLength
        if self.autoStarted:
            effectiveDemoLength -= self.autoStarted
        self.splits.append(("Done", effectiveDemoLength))
        

    def getDemoInfo(self):
        printInfo = {}
        printInfo["Player"] =  self.headerFieldValues["clientName"]
        if self.headerFieldValues["mapName"] in conversions.chamberNames.keys():
            printInfo["Level"] = conversions.chamberNames[self.headerFieldValues["mapName"]]
        else:
            printInfo["Map"] = self.headerFieldValues["mapName"]
        for field in printInfo:
            print(field+(20-len(field))*" "+":", printInfo[field])
        print()
        print("Measured Time"+7*" "+":", round(self.demoLength*0.015, 3))
        print("Measured Ticks"+6*" "+":", self.demoLength)
        adjustedTicks = self.demoLength
        if self.autoStarted:
            adjustedTicks -= self.autoStarted
        if self.autoEnded:
            adjustedTicks -= (self.demoLength-self.autoEnded)

        if adjustedTicks != self.demoLength:
            print("Adjusted Time"+7*" "+":", round(adjustedTicks*0.015, 3))
            print("Adjusted Ticks"+6*" "+":", adjustedTicks)



    def showSplits(self):
        tableData = [["Split name", "Segment time", "Split time"]]
        previousSplit = 0
        for split in self.splits:
            splitTicks = split[1]
            segmentTicks = split[1]-previousSplit
            previousSplit = splitTicks
            splitTime = round(splitTicks*0.015, 3)
            segmentTime = round(segmentTicks*0.015, 3)
            tableData.append([split[0], str(segmentTime), str(splitTime)])

        output = neatTables.generateTable(tableData)
        return output

        
            


    def pullField(self, fieldDict: dict, stream: bitstring.BitStream) -> str | int | float:
        """
        Extract the value of a field from the bitstream, using a dict as a guide as to how to do it
        Arguments:
            fieldDict - The guide dict, in the format {"index": 0, "length": 16, "type": "int"}
            stream - The bitstream to extract the data from
        Returns:
            Type is determined by the fieldDict type, returns the value of the field.
        """

        data = stream[fieldDict["index"]:fieldDict["index"]+fieldDict["length"]]

        match fieldDict["type"]:
            case "str":
                return data.bytes.decode("utf-8").rstrip('\x00')
            
            case "int":
                return data.intle
            
            case "float":
                return data.floatle
            
    
    def parseMessage(self, offset: int, stream: bitstring.BitStream) -> Message:
        """
        Parse the next message given an offset.
        Arguments:
            offset - the offset into the bitstream, given in bits
            stream - the bitstream containing the messages
        Returns:
            An object of varying type based on the type of the message, always a subclass of Message
        """
        messageTypeID = stream[offset:offset+8].intle # Extract the first byte to see message type
        messageType = conversions.messageTables[messageTypeID] # Convert to human readable type
        match messageType:
            case "Packet" | "SignOn":
                return PacketMessage(offset, stream)
            
            case "SyncTick":
                return SyncTickMessage(offset, stream)
            
            case "ConsoleCmd":
                return ConsoleCommandMessage(offset, stream)
            
            case "UserCmd":
                return UserCommandMessage(offset, stream)
            
            case "DataTables":
                return DataTablesMessage(offset, stream)
        
            case "Stop":
                return None

            case "StringTables":
                return StringTablesMessage(offset, stream)


if __name__ == "__main__":
    demo = DemoParse("your/demo/here.dem")
    print(demo.showSplits())

