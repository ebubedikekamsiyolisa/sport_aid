import customtkinter as ctk
from tkinter import messagebox
from app.database.database import DatabaseManager


class SettingsView(ctk.CTkFrame):
    """
    Manages the biometrics profile view, allowing users to save their weight
    which is critical for accurate personalized MET calculations.
    """

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#1A1A1A", corner_radius=0)
        self.controller = controller
        self.db = DatabaseManager()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_profile_form()
        self.load_profile_data()

    def _build_profile_form(self):
        """Assembles a clean workspace card to securely record biographical values."""
        card = ctk.CTkFrame(self, fg_color="#2E2E2E", corner_radius=12, width=500)
        card.grid(row=0, column=0, padx=40, pady=40, sticky="n")

        title = ctk.CTkLabel(card, text="👤 User Profile & Biometrics Settings",
                             font=ctk.CTkFont(size=20, weight="bold"), text_color="#FFFFFF")
        title.pack(anchor="w", padx=30, pady=(30, 5))

        subtitle = ctk.CTkLabel(card,
                                text="Your biometrics are stored locally and are used to calculate calorie estimates.",
                                font=ctk.CTkFont(size=12), text_color="#A1A1AA")
        subtitle.pack(anchor="w", padx=30, pady=(0, 20))

        lbl_name = ctk.CTkLabel(card, text="Display Name *", font=ctk.CTkFont(size=13), text_color="#A1A1AA")
        lbl_name.pack(anchor="w", padx=30, pady=2)
        self.entry_name = ctk.CTkEntry(card, placeholder_text="e.g. Jane Doe", height=38, fg_color="#1A1A1A",
                                       border_color="#A1A1AA", width=400)
        self.entry_name.pack(padx=30, pady=(0, 15))

        lbl_weight = ctk.CTkLabel(card, text="Weight (kg) *", font=ctk.CTkFont(size=13), text_color="#A1A1AA")
        lbl_weight.pack(anchor="w", padx=30, pady=2)
        self.entry_weight = ctk.CTkEntry(card, placeholder_text="e.g. 70.5", height=38, fg_color="#1A1A1A",
                                         border_color="#A1A1AA", width=400)
        self.entry_weight.pack(padx=30, pady=(0, 15))

        lbl_age = ctk.CTkLabel(card, text="Age *", font=ctk.CTkFont(size=13), text_color="#A1A1AA")
        lbl_age.pack(anchor="w", padx=30, pady=2)
        self.entry_age = ctk.CTkEntry(card, placeholder_text="e.g. 25", height=38, fg_color="#1A1A1A",
                                      border_color="#A1A1AA", width=400)
        self.entry_age.pack(padx=30, pady=(0, 15))

        lbl_gender = ctk.CTkLabel(card, text="Gender *", font=ctk.CTkFont(size=13), text_color="#A1A1AA")
        lbl_gender.pack(anchor="w", padx=30, pady=2)
        self.combo_gender = ctk.CTkComboBox(card, values=["Male", "Female", "Other"], height=38, fg_color="#1A1A1A",
                                            border_color="#A1A1AA", width=400)
        self.combo_gender.pack(padx=30, pady=(0, 25))

        btn_save = ctk.CTkButton(
            card, text="🔒 Save Biometrics Profile", height=42, corner_radius=8,
            fg_color="#22C55E", hover_color="#16A34A", text_color="#FFFFFF", font=ctk.CTkFont(weight="bold"),
            command=self._handle_save_profile
        )
        btn_save.pack(fill="x", padx=30, pady=(0, 30))

    def _handle_save_profile(self):
        """Validates entry files and updates the database state row securely."""
        name = self.entry_name.get().strip()
        raw_weight = self.entry_weight.get().strip()
        raw_age = self.entry_age.get().strip()
        gender = self.combo_gender.get()

        if not name or not raw_weight or not raw_age:
            messagebox.showerror("Validation Error", "All fields with an asterisk (*) are mandatory.")
            return

        try:
            weight = float(raw_weight)
            age = int(raw_age)
            if weight <= 20 or weight > 300 or age <= 5 or age > 120:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Validation Error", "Please provide a realistic weight (20-300kg) and age (5-120).")
            return

        try:
            # Upsert design: clean existing records first, then maintain exactly one profile row
            self.db.execute_write("DELETE FROM user_profile")
            self.db.execute_write(
                "INSERT INTO user_profile (name, weight_kg, age, gender) VALUES (?, ?, ?, ?)",
                (name, weight, age, gender)
            )
            messagebox.showinfo("Profile Updated", "Your local biometrics settings were saved successfully!")
            self.load_profile_data()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to save profile: {e}")

    def load_profile_data(self):
        """Loads saved biometrics out of SQLite directly into the active fields."""
        try:
            rows = self.db.execute_read("SELECT * FROM user_profile LIMIT 1")
            if rows:
                profile = rows[0]
                self.entry_name.delete(0, 'end')
                self.entry_name.insert(0, profile['name'])
                self.entry_weight.delete(0, 'end')
                self.entry_weight.insert(0, str(profile['weight_kg']))
                self.entry_age.delete(0, 'end')
                self.entry_age.insert(0, str(profile['age']))
                self.combo_gender.set(profile['gender'])
        except Exception:
            pass