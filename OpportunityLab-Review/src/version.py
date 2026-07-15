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
            f"{self.app_name} {self.version} | "
            f"{self.package} | "
            f"Build {self.build} | "
            f"{self.codename} | "
            f"{self.status}"
        )


VERSION_INFO = VersionInfo(
    app_name="OpportunityLab",
    version="0.20.0",
    package="Package-020A-01",
    build=1,
    codename="Trailblazer",
    status="Development",
)
