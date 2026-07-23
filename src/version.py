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
    "1.0.0",
    "Package-100A-08",
    10,
    "Gold Rush",
    "Production",
)
