from dataclasses import dataclass


@dataclass(frozen=True)
class VersionInfo:
    app_name: str
    version: str
    package: str
    build: int
    codename: str
    status: str

    @property
    def window_title(self) -> str:
        return f"{self.app_name} {self.version}"

    @property
    def full_label(self) -> str:
        return (
            f"{self.app_name} {self.version} | {self.package} | "
            f"Build {self.build} | {self.codename} | {self.status}"
        )


VERSION_INFO = VersionInfo(
    app_name="OpportunityLab",
    version="0.22.0",
    package="Package-022A-02",
    build=2,
    codename="Pathfinder",
    status="Development",
)
