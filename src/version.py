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
    def window_title(self):
        return f"{self.app_name} {self.version}"

    @property
    def full_label(self):
        return (
            f"{self.app_name} {self.version} | {self.package} | "
            f"Build {self.build} | {self.codename} | {self.status}"
        )


VERSION_INFO = VersionInfo(
    "OpportunityLab",
    "1.1.0",
    "Package-110A-01",
    1,
    "Gold Rush",
    "Production",
)
