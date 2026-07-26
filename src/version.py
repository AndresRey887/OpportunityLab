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
    "1.0.4",
    "Package-100B-04",
    15,
    "Gold Rush",
    "Production",
)
