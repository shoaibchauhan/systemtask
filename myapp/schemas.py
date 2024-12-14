from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ProcessInfo(BaseModel):
    name: Optional[str]
    username: Optional[str]
    pid: int
    create_time: datetime

class ProcessDataRequest(BaseModel):
    system_name: str
    processes: List[ProcessInfo]
    timestamp: datetime
    


class ProcessDataResponse(BaseModel):
    system_name: str
    process_name: str
    username: str
    pid: int
    create_time: datetime
    timestamp: datetime

    class Config:
        orm_mode = True  # This allows Pydantic to work with ORM models