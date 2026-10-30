from pages.add_match import AddMatchPage
from pages.dashboard import DashboardPage
from pages.settings import SettingsPage

PAGE_REGISTRY = {
    "Dashboard": DashboardPage,
    "Add Match": AddMatchPage,
    "Settings": SettingsPage,
}

__all__ = ["AddMatchPage", "DashboardPage", "PAGE_REGISTRY", "SettingsPage"]