import customtkinter as ctk
from app.ui.dashboard import DashboardView
from app.ui.activities import ActivitiesView
from app.ui.routines import RoutinesView
from app.ui.settings import SettingsView
from app.ui.progress import ProgressView
from app.ui.workout import WorkoutTrackView


class Sport_aidApp(ctk.CTk):
    """
    The central structural application shell and window controller for Sport_aid.
    Establishes dark-mode layout parameters and global layout sync routing passes.
    """

    def __init__(self):
        super().__init__()

        # --- DESIGN SYSTEM & LAYOUT CONSTRAINTS ---
        self.title("Sport_aid — Sports & Fitness Routine Manager")
        self.geometry("1100x680")

        # Enforce rigid minimizations floor limits to prevent responsive layout damage
        self.minsize(980, 620)

        # Force Dark Tech Aesthetic theme rules
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("green")

        # --- COLUMN WIDTH LAYOUT SCHEMAS ---
        self.grid_columnconfigure(0, weight=0)  # Sidebar locked frame width
        self.grid_columnconfigure(1, weight=1)  # Workspace expands
        self.grid_rowconfigure(0, weight=1)

        # --- UI LAYOUT ASSEMBLY ---
        self._build_sidebar_navigation()
        self._build_workspace_canvas()

        # Default focus view target routing
        self._select_navigation_view("dashboard")

    def _build_sidebar_navigation(self):
        """Creates the sidebar container panel and all structural navigational buttons."""
        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=0, width=220, fg_color="#2E2E2E")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(7, weight=1)

        # Glowing brand header text logo string
        self.app_title = ctk.CTkLabel(
            self.sidebar_frame,
            text="SPORT_AID",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color="#A3E635"
        )
        self.app_title.grid(row=0, column=0, padx=20, pady=25, sticky="w")

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
        """Instantiates all real production views stacked inside our display canvas space."""
        self.views = {}

        self.views["dashboard"] = DashboardView(parent=self, controller=self)
        self.views["activities"] = ActivitiesView(parent=self, controller=self)
        self.views["routines"] = RoutinesView(parent=self, controller=self)
        self.views["settings"] = SettingsView(parent=self, controller=self)
        self.views["progress"] = ProgressView(parent=self, controller=self)
        self.views["track"] = WorkoutTrackView(parent=self, controller=self)

    def _select_navigation_view(self, view_name: str):
        """Manages router states, highlights sidebar active states, and updates live database data streams."""
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

        # --- DYNAMIC INTERFACE SYNCHRONIZATION HOOKS ---
        if hasattr(self.views[view_name], "refresh_dashboard_data"):
            self.views[view_name].refresh_dashboard_data()
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