import bitstring
import conversions

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
        self.bits_dataSize = self.stream[self.offset+89*8:self.offset+93*8].intle*8
        
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
    def __init__(self, filePath):
        with open(filePath, 'rb') as f:
            stream = bitstring.BitStream(bytes=f.read())
        
        # Get demo header
        headerFieldValues = {}

        for field in conversions.headerFields.keys():
            headerFieldValues[field] = self.pullField(conversions.headerFields[field], stream)

        fileSize = len(stream)
        currentOffset = 1072*8 # The end of the header/start of the data (in bits)
        # Number of iterations is not
        self.demoLength = 0
        endReached = False
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
                        endReached = True
                        self.demoLength += 1 # idk why adding one is necessary but it is

                if parsedMessage.type == "UserCmd":
                    if not endReached:
                        self.demoLength += 1
                currentOffset += parsedMessage.bits_size

        self.demoLength += 1 # 0th tick xD
        



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



print(DemoParse("08-1163.dem").demoLength)