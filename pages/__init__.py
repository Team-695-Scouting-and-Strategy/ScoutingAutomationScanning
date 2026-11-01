from pages.add_match import AddMatchPage
from pages.dashboard import DashboardPage
from pages.settings import SettingsPage
from pages.analytics import AnalyticsPage

PAGE_REGISTRY = {
    "Dashboard": DashboardPage,
    "Add Match": AddMatchPage,
    "Settings": SettingsPage,
    "Analytics": AnalyticsPage,
}

__all__ = ["AddMatchPage", "DashboardPage", "PAGE_REGISTRY", "SettingsPage"]