class ContextInfo:
    def __init__(self):
        self.tag=''
        self.symbol=''
        self.org=''
        self.error=''
        self.status=False
    
    def clear(self):
        self.__init__()
        
    def set( self,tag, symbol,org, error,status):
        self.tag=tag
        self.symbol=symbol
        self.org=org
        self.error=error
        self.status=status
    
    def serialize(self):
        return {"tag": self.tag,
                "symbol": self.symbol,
                "org": self.org,
                "error": self.error,
                "status": self.status}