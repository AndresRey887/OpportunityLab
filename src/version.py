from dataclasses import dataclass


@dataclass(frozen=True)
class VersionInfo:
    app_name: str
    version: str
    package: str
    build: int
    codename: str
    status: str


VERSION_INFO = VersionInfo(
    app_name="OpportunityLab",
    version="0.20.0",
    package="Package-020A-09",
    build=9,
    codename="Trailblazer",
    status="Development",
)
