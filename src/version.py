
from dataclasses import dataclass
@dataclass(frozen=True)
class VersionInfo:
    app_name:str;version:str;package:str;build:int;codename:str;status:str
VERSION_INFO=VersionInfo("OpportunityLab","0.20.0","Package-020A-08",8,"Trailblazer","Development")
