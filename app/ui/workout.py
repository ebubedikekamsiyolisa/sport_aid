import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from app.database.database import DatabaseManager
from app.services.calorie_calculator import CalorieCalculator


class WorkoutTrackView(ctk.CTkFrame):
    """
    Manages active workout session execution. Allows selection of a pre-made
    routine shell, guides the user step-by-step through exercises, and auto-logs
    the completed workout into the database history.
    """

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#1A1A1A", corner_radius=0)
        self.controller = controller
        self.db = DatabaseManager()

        # Session tracking state variables
        self.active_routine = None
        self.exercises = []
        self.current_idx = 0
        self.accumulated_duration_mins = 0

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Draw the initial routine selection panel state
        self.render_routine_selector_screen()

    def render_routine_selector_screen(self):
        """Builds the drop-down routine landing page configuration selection state."""
        self._clear_view_canvas()

        selector_card = ctk.CTkFrame(self, fg_color="#2E2E2E", corner_radius=12)
        selector_card.grid(row=0, column=0, padx=40, pady=40, sticky="n")

        title = ctk.CTkLabel(selector_card, text="⏱️ Start Active Workout Session",
                             font=ctk.CTkFont(size=20, weight="bold"), text_color="#FFFFFF")
        title.pack(anchor="w", padx=30, pady=(30, 5))

        subtitle = ctk.CTkLabel(selector_card,
                                text="Select a pre-configured routine blueprint to track your performance step-by-step.",
                                font=ctk.CTkFont(size=12), text_color="#A1A1AA")
        subtitle.pack(anchor="w", padx=30, pady=(0, 20))

        lbl_select = ctk.CTkLabel(selector_card, text="Choose Routine Blueprint *", font=ctk.CTkFont(size=13),
                                  text_color="#A1A1AA")
        lbl_select.pack(anchor="w", padx=30, pady=2)

        self.combo_routines = ctk.CTkComboBox(selector_card, values=[], height=38, fg_color="#1A1A1A",
                                              border_color="#A1A1AA", width=400)
        self.combo_routines.pack(padx=30, pady=(0, 25))

        btn_start = ctk.CTkButton(
            selector_card, text="🚀 Launch Workout Session", height=42, corner_radius=8,
            fg_color="#0EA5E9", hover_color="#0284C7", text_color="#FFFFFF", font=ctk.CTkFont(weight="bold"),
            command=self._handle_initialize_session
        )
        btn_start.pack(fill="x", padx=30, pady=(0, 30))

        self.reload_available_routines()

    def reload_available_routines(self):
        """Populates the routine drop-down list from the SQLite database."""
        try:
            rows = self.db.execute_read("SELECT name FROM routines ORDER BY name ASC")
            names = [r['name'] for r in rows]
            self.combo_routines.configure(values=names)
            if names:
                self.combo_routines.set(names[0])
        except Exception:
            pass

    def _handle_initialize_session(self):
        """Fetches the routine and its nested exercises to transition into the active workspace."""
        selected_name = self.combo_routines.get()
        if not selected_name:
            messagebox.showerror("Selection Error", "Please create a workout routine blueprint before tracking.")
            return

        try:
            routine_row = self.db.execute_read("SELECT id FROM routines WHERE name = ?", (selected_name,))
            if not routine_row:
                return

            self.active_routine = {"id": routine_row[0]['id'], "name": selected_name}

            # Fetch relational exercises linking down from this profile ID
            ex_rows = self.db.execute_read(
                "SELECT * FROM routine_exercises WHERE routine_id = ? ORDER BY order_index ASC",
                (self.active_routine["id"],)
            )

            self.exercises = [dict(r) for r in ex_rows]

            if not self.exercises:
                messagebox.showwarning("Empty Routine",
                                       f"'{selected_name}' has no exercises. Please append items to this routine first.")
                return

            # Reset state and step into wizard workflow state
            self.current_idx = 0
            self.accumulated_duration_mins = 0
            self.render_active_step_wizard()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to mount session: {e}")

    def render_active_step_wizard(self):
        """Renders the high-fidelity tracking dashboard wizard interface view frame."""
        self._clear_view_canvas()

        current_exercise = self.exercises[self.current_idx]

        wizard_card = ctk.CTkFrame(self, fg_color="#2E2E2E", corner_radius=12)
        wizard_card.grid(row=0, column=0, padx=30, pady=30, sticky="nsew")
        wizard_card.grid_columnconfigure(0, weight=1)

        # Upper progress tracking breadcrumb bar
        progress_text = f"EXERCISE {self.current_idx + 1} OF {len(self.exercises)}  |  Active Routine: {self.active_routine['name'].upper()}"
        lbl_prog = ctk.CTkLabel(wizard_card, text=progress_text, font=ctk.CTkFont(size=12, weight="bold"),
                                text_color="#A3E635")
        lbl_prog.pack(anchor="w", padx=30, pady=(25, 5))

        # Main prominent exercise label string title
        lbl_ex_name = ctk.CTkLabel(wizard_card, text=current_exercise['exercise_name'],
                                   font=ctk.CTkFont(size=28, weight="bold"), text_color="#FFFFFF")
        lbl_ex_name.pack(anchor="w", padx=30, pady=10)

        # Targets panel layout frame block
        targets_strip = ctk.CTkFrame(wizard_card, fg_color="#1A1A1A", corner_radius=8)
        targets_strip.pack(fill="x", padx=30, pady=15)

        spec_labels = []
        if current_exercise['target_duration_seconds'] > 0:
            spec_labels.append(f"⏱️ Duration Target: {current_exercise['target_duration_seconds']} seconds")
        if current_exercise['target_reps'] > 0:
            spec_labels.append(f"🔢 Repetitions Target: {current_exercise['target_reps']} reps")
        if not spec_labels:
            spec_labels.append("🏋️‍♂️ Standard Target Set")

        lbl_spec = ctk.CTkLabel(targets_strip, text="  •  ".join(spec_labels), font=ctk.CTkFont(size=14, weight="bold"),
                                text_color="#0EA5E9")
        lbl_spec.pack(pady=15)

        # Form entry input to simulate localized actual duration minutes spent per step
        input_container = ctk.CTkFrame(wizard_card, fg_color="transparent")
        input_container.pack(fill="x", padx=30, pady=10)

        lbl_time = ctk.CTkLabel(input_container, text="Estimated minutes spent on this exercise *",
                                font=ctk.CTkFont(size=13), text_color="#A1A1AA")
        lbl_time.pack(anchor="w", pady=2)
        self.entry_step_time = ctk.CTkEntry(input_container, placeholder_text="e.g. 5", height=38, fg_color="#1A1A1A",
                                            border_color="#A1A1AA")
        self.entry_step_time.pack(fill="x")
        self.entry_step_time.insert(0, "5")  # Sensible standard value injection

        # Bottom navigation action tools controls layout row strip
        btn_strip = ctk.CTkFrame(wizard_card, fg_color="transparent")
        btn_strip.pack(fill="x", padx=30, pady=(30, 25), side="bottom")

        # Contextual text routing depending if there is a next step or completion event
        is_final_step = (self.current_idx == len(self.exercises) - 1)
        next_btn_text = "🏁 Finish Workout Session" if is_final_step else "➡️ Next Exercise"
        next_btn_color = "#22C55E" if is_final_step else "#0EA5E9"

        btn_next = ctk.CTkButton(
            btn_strip, text=next_btn_text, height=42, corner_radius=8,
            fg_color=next_btn_color, hover_color="#16A34A" if is_final_step else "#0284C7", text_color="#FFFFFF",
            font=ctk.CTkFont(weight="bold"), command=self._handle_advance_wizard_step
        )
        btn_next.pack(side="right", padx=(10, 0), expand=True, fill="x")

        if self.current_idx > 0:
            btn_prev = ctk.CTkButton(
                btn_strip, text="⬅️ Back", height=42, corner_radius=8,
                fg_color="transparent", border_color="#A1A1AA", border_width=1, text_color="#FFFFFF",
                command=self._handle_regress_wizard_step
            )
            btn_prev.pack(side="left", padx=(0, 10), expand=True, fill="x")

    def _handle_advance_wizard_step(self):
        """Validates step form logs, updates telemetry counters, and manages step progression transitions."""
        raw_time = self.entry_step_time.get().strip()
        try:
            mins = int(raw_time)
            if mins <= 0: raise ValueError()
        except ValueError:
            messagebox.showerror("Validation Error", "Please provide a valid whole number greater than 0.")
            return

        self.accumulated_duration_mins += mins

        # Branch processing checking if we hit completion limits
        if self.current_idx < len(self.exercises) - 1:
            self.current_idx += 1
            self.render_active_step_wizard()
        else:
            self._execute_commit_completed_session_to_db()

    def _handle_regress_wizard_step(self):
        """Regresses wizard states back one indexing item row layout frame."""
        if self.current_idx > 0:
            self.current_idx -= 1
            self.render_active_step_wizard()

    def _execute_commit_completed_session_to_db(self):
        """Computes summary metrics values and logs the finalized routine into the SQLite data tables."""
        today_str = datetime.now().strftime("%Y-%m-%d")

        # Calculate calorie values using our new scientific service module
        weight_kg = 70.0
        try:
            prof = self.db.execute_read("SELECT weight_kg FROM user_profile LIMIT 1")
            if prof: weight_kg = prof[0]['weight_kg']
        except Exception:
            pass
            # --- This section lives inside a tracking completion method (like _finish_workout) ---
            calories = CalorieCalculator.calculate("Custom Routine", self.accumulated_duration_mins, weight_kg)

            query = """
                   INSERT INTO activities (activity_type, duration_minutes, distance_km, steps, calories_burned, log_date, notes)
                   VALUES (?, ?, 0, 0, ?, ?, ?)
               """

            notes = f"Completed pre-made routine plan tracking: {self.active_routine['name']}"

            try:
                self.db.execute_write(
                    query,
                    (f"Routine: {self.active_routine['name']}", self.accumulated_duration_mins, calories, today_str,
                     notes)
                )

                messagebox.showinfo(
                    "Workout Complete!",
                    f"Congratulations! You tracked {len(self.exercises)} exercises across {self.accumulated_duration_mins} total active minutes.\nSession saved to history!"
                )

                # Reset state and step clean back out to initial selector view screen canvas
                self.render_routine_selector_screen()

            except Exception as e:
                messagebox.showerror("Database Error", f"Failed to register completed routine trace: {e}")

    def _clear_view_canvas(self):
        """Wipes out active interior child widgets painted inside the frame canvas space."""
        for widget in self.winfo_children():
            widget.destroy()