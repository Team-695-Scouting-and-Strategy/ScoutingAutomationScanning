from views.add_team import AddTeamView
from views.dashboard import DashboardView
from views.settings import SettingsView
from views.analytics import AnalyticsView

VIEW_REGISTRY = {
    "Dashboard": DashboardView,
    "Add Team": AddTeamView,
    "Settings": SettingsView,
    "Analytics": AnalyticsView,
}

__all__ = ["AddTeamView", "DashboardView", "SettingsView", "VIEW_REGISTRY"]