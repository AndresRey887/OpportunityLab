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
    version="0.21.0",
    package="Package-021A-08",
    build=8,
    codename="Catalyst",
    status="Development",
)
