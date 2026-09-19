import customtkinter as ctk
from app.ui.dashboard import DashboardView
from app.ui.activities import ActivitiesView
from app.ui.routines import RoutinesView
from app.ui.settings import SettingsView
from app.ui.progress import ProgressView
from app.ui.workout import WorkoutTrackView


class Sport_aidApp(ctk.CTk):
    """
    The main Application Frame and window controller for Sport_aid.
    Establishes the design tokens, window bounds, sidebar navigation layout,
    and view-switching routing mechanism.
    """

    def __init__(self):
        super().__init__()

        # --- DESIGN SYSTEM & SYSTEM CONFIGURATION ---
        self.title("Sport_aid — Sports & Fitness Routine Manager")
        self.geometry("1100x680")
        self.minsize(950, 600)

        # Enforce dark theme guidelines
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("green")

        # --- WINDOW GRID CONFIGURATION ---
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- UI LAYOUT ASSEMBLY ---
        self._build_sidebar_navigation()
        self._build_workspace_canvas()

        # Initialize by selecting the Dashboard default panel
        self._select_navigation_view("dashboard")

    def _build_sidebar_navigation(self):
        """Creates the sidebar container panel and all structural navigational buttons."""
        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=0, width=220, fg_color="#2E2E2E")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(7, weight=1)

        # App Brand Title Header Text
        self.app_title = ctk.CTkLabel(
            self.sidebar_frame,
            text="SPORT_AID",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color="#A3E635"
        )
        self.app_title.grid(row=0, column=0, padx=20, pady=25, sticky="w")

        # Define all navigation links to assemble
        self.nav_buttons = {}
        nav_items = [
            ("dashboard", "🏠  Dashboard", 1),
            ("routines", "📋  My Routines", 2),
            ("activities", "🏃‍♂️  Activities", 3),
            ("track", "⏱️  Track Workout", 4),
            ("progress", "📊  Progress", 5),
            ("settings", "⚙️  Settings", 6)
        ]

        for key, text, row_idx in nav_items:
            btn = ctk.CTkButton(
                self.sidebar_frame,
                text=text,
                height=40,
                corner_radius=8,
                fg_color="transparent",
                text_color="#A1A1AA",
                anchor="w",
                font=ctk.CTkFont(family="Segoe UI", size=14, weight="normal"),
                command=lambda k=key: self._select_navigation_view(k)
            )
            btn.grid(row=row_idx, column=0, padx=15, pady=6, sticky="ew")
            self.nav_buttons[key] = btn

    def _build_workspace_canvas(self):
        """Creates individual workspace view frames stacked inside column 1."""
        self.views = {}

        # Instantiate production views
        self.views["dashboard"] = DashboardView(parent=self, controller=self)
        self.views["activities"] = ActivitiesView(parent=self, controller=self)
        self.views["routines"] = RoutinesView(parent=self, controller=self)
        self.views["settings"] = SettingsView(parent=self, controller=self)
        self.views["progress"] = ProgressView(parent=self, controller=self)
        self.views["track"] = WorkoutTrackView(parent=self, controller=self)

    def _select_navigation_view(self, view_name: str):
        """Manages router states, updates sidebar active states, and displays correct views."""
        for key, button in self.nav_buttons.items():
            button.configure(fg_color="transparent", text_color="#A1A1AA", font=ctk.CTkFont(weight="normal"))

        if view_name in self.nav_buttons:
            self.nav_buttons[view_name].configure(
                fg_color="#0EA5E9",
                text_color="#FFFFFF",
                font=ctk.CTkFont(weight="bold")
            )

        for frame in self.views.values():
            frame.grid_forget()

        # Dynamic data reload distribution sweeps
        if hasattr(self.views[view_name], "refresh_logs_display"):
            self.views[view_name].refresh_logs_display()
        if hasattr(self.views[view_name], "reload_routines_context"):
            self.views[view_name].reload_routines_context()
        if hasattr(self.views[view_name], "load_profile_data"):
            self.views[view_name].load_profile_data()
        if hasattr(self.views[view_name], "refresh_statistics_metrics"):
            self.views[view_name].refresh_statistics_metrics()
        if hasattr(self.views[view_name], "reload_available_routines"):
            self.views[view_name].reload_available_routines()

        self.views[view_name].grid(row=0, column=1, sticky="nsew")