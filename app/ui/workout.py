import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

from app.database.database import DatabaseManager
from app.services.calorie_calculator import CalorieCalculator


class WorkoutTrackView(ctk.CTkFrame):
    """
    Manages active workout session execution.

    Allows the user to:
    - Select a pre-made workout routine
    - Move through exercises step-by-step
    - Enter the time spent on each exercise
    - Calculate total workout duration and calories
    - Save the completed workout to the activities table
    """

    def __init__(self, parent, controller):
        super().__init__(
            parent,
            fg_color="#1A1A1A",
            corner_radius=0
        )

        self.controller = controller
        self.db = DatabaseManager()

        # Active workout state
        self.active_routine = None
        self.exercises = []
        self.current_idx = 0
        self.accumulated_duration_mins = 0

        # Store entered duration for each exercise.
        # This prevents values from being lost when using Back.
        self.exercise_durations = {}

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.render_routine_selector_screen()

    # ------------------------------------------------------------------
    # ROUTINE SELECTION
    # ------------------------------------------------------------------

    def render_routine_selector_screen(self):
        """Displays the routine selection screen."""

        self._clear_view_canvas()

        selector_card = ctk.CTkFrame(
            self,
            fg_color="#2E2E2E",
            corner_radius=12
        )
        selector_card.grid(
            row=0,
            column=0,
            padx=40,
            pady=40,
            sticky="n"
        )

        title = ctk.CTkLabel(
            selector_card,
            text="⏱️ Start Active Workout Session",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#FFFFFF"
        )
        title.pack(
            anchor="w",
            padx=30,
            pady=(30, 5)
        )

        subtitle = ctk.CTkLabel(
            selector_card,
            text=(
                "Select a pre-configured routine blueprint "
                "to track your performance step-by-step."
            ),
            font=ctk.CTkFont(size=12),
            text_color="#A1A1AA"
        )
        subtitle.pack(
            anchor="w",
            padx=30,
            pady=(0, 20)
        )

        lbl_select = ctk.CTkLabel(
            selector_card,
            text="Choose Routine Blueprint *",
            font=ctk.CTkFont(size=13),
            text_color="#A1A1AA"
        )
        lbl_select.pack(
            anchor="w",
            padx=30,
            pady=2
        )

        self.combo_routines = ctk.CTkComboBox(
            selector_card,
            values=[],
            height=38,
            fg_color="#1A1A1A",
            border_color="#A1A1AA",
            width=400
        )
        self.combo_routines.pack(
            padx=30,
            pady=(0, 25)
        )

        btn_start = ctk.CTkButton(
            selector_card,
            text="🚀 Launch Workout Session",
            height=42,
            corner_radius=8,
            fg_color="#0EA5E9",
            hover_color="#0284C7",
            text_color="#FFFFFF",
            font=ctk.CTkFont(weight="bold"),
            command=self._handle_initialize_session
        )
        btn_start.pack(
            fill="x",
            padx=30,
            pady=(0, 30)
        )

        self.reload_available_routines()

    def reload_available_routines(self):
        """Loads available workout routines from the database."""

        try:
            rows = self.db.execute_read(
                "SELECT name FROM routines ORDER BY name ASC"
            )

            names = [r["name"] for r in rows]

            self.combo_routines.configure(values=names)

            if names:
                self.combo_routines.set(names[0])

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                f"Failed to load workout routines:\n{e}"
            )

    def _handle_initialize_session(self):
        """Loads the selected routine and starts the workout wizard."""

        selected_name = self.combo_routines.get().strip()

        if not selected_name:
            messagebox.showerror(
                "Selection Error",
                "Please create a workout routine blueprint before tracking."
            )
            return

        try:
            routine_row = self.db.execute_read(
                "SELECT id FROM routines WHERE name = ?",
                (selected_name,)
            )

            if not routine_row:
                messagebox.showerror(
                    "Routine Error",
                    "The selected routine could not be found."
                )
                return

            self.active_routine = {
                "id": routine_row[0]["id"],
                "name": selected_name
            }

            ex_rows = self.db.execute_read(
                """
                SELECT *
                FROM routine_exercises
                WHERE routine_id = ?
                ORDER BY order_index ASC
                """,
                (self.active_routine["id"],)
            )

            self.exercises = [dict(row) for row in ex_rows]

            if not self.exercises:
                messagebox.showwarning(
                    "Empty Routine",
                    (
                        f"'{selected_name}' has no exercises. "
                        "Please append exercises to this routine first."
                    )
                )
                return

            # Reset workout state
            self.current_idx = 0
            self.accumulated_duration_mins = 0
            self.exercise_durations = {}

            self.render_active_step_wizard()

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Failed to start workout session:\n{e}"
            )

    # ------------------------------------------------------------------
    # ACTIVE WORKOUT WIZARD
    # ------------------------------------------------------------------

    def render_active_step_wizard(self):
        """Displays the current exercise."""

        self._clear_view_canvas()

        if not self.exercises:
            return

        current_exercise = self.exercises[self.current_idx]

        wizard_card = ctk.CTkFrame(
            self,
            fg_color="#2E2E2E",
            corner_radius=12
        )

        wizard_card.grid(
            row=0,
            column=0,
            padx=30,
            pady=30,
            sticky="nsew"
        )

        wizard_card.grid_columnconfigure(0, weight=1)

        # Progress
        progress_text = (
            f"EXERCISE {self.current_idx + 1} OF {len(self.exercises)}"
            f"  |  Active Routine: "
            f"{self.active_routine['name'].upper()}"
        )

        lbl_prog = ctk.CTkLabel(
            wizard_card,
            text=progress_text,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#A3E635"
        )
        lbl_prog.pack(
            anchor="w",
            padx=30,
            pady=(25, 5)
        )

        # Exercise name
        exercise_name = current_exercise.get(
            "exercise_name",
            "Unnamed Exercise"
        )

        lbl_ex_name = ctk.CTkLabel(
            wizard_card,
            text=exercise_name,
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#FFFFFF"
        )
        lbl_ex_name.pack(
            anchor="w",
            padx=30,
            pady=10
        )

        # Target information
        targets_strip = ctk.CTkFrame(
            wizard_card,
            fg_color="#1A1A1A",
            corner_radius=8
        )
        targets_strip.pack(
            fill="x",
            padx=30,
            pady=15
        )

        spec_labels = []

        target_duration = current_exercise.get(
            "target_duration_seconds",
            0
        )

        target_reps = current_exercise.get(
            "target_reps",
            0
        )

        if target_duration and target_duration > 0:
            spec_labels.append(
                f"⏱️ Duration Target: {target_duration} seconds"
            )

        if target_reps and target_reps > 0:
            spec_labels.append(
                f"🔢 Repetitions Target: {target_reps} reps"
            )

        if not spec_labels:
            spec_labels.append("🏋️ Standard Target Set")

        lbl_spec = ctk.CTkLabel(
            targets_strip,
            text="  •  ".join(spec_labels),
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#0EA5E9"
        )
        lbl_spec.pack(pady=15)

        # Duration input
        input_container = ctk.CTkFrame(
            wizard_card,
            fg_color="transparent"
        )
        input_container.pack(
            fill="x",
            padx=30,
            pady=10
        )

        lbl_time = ctk.CTkLabel(
            input_container,
            text="Estimated minutes spent on this exercise *",
            font=ctk.CTkFont(size=13),
            text_color="#A1A1AA"
        )
        lbl_time.pack(
            anchor="w",
            pady=2
        )

        self.entry_step_time = ctk.CTkEntry(
            input_container,
            placeholder_text="e.g. 5",
            height=38,
            fg_color="#1A1A1A",
            border_color="#A1A1AA"
        )
        self.entry_step_time.pack(fill="x")

        # Restore previously entered value when going back
        previous_value = self.exercise_durations.get(
            self.current_idx,
            5
        )

        self.entry_step_time.insert(
            0,
            str(previous_value)
        )

        # Navigation buttons
        btn_strip = ctk.CTkFrame(
            wizard_card,
            fg_color="transparent"
        )
        btn_strip.pack(
            fill="x",
            padx=30,
            pady=(30, 25)
        )

        is_final_step = (
            self.current_idx == len(self.exercises) - 1
        )

        if is_final_step:
            next_btn_text = "🏁 Finish Workout Session"
            next_btn_color = "#22C55E"
            hover_color = "#16A34A"
        else:
            next_btn_text = "➡️ Next Exercise"
            next_btn_color = "#0EA5E9"
            hover_color = "#0284C7"

        # FINISH / NEXT BUTTON
        btn_next = ctk.CTkButton(
            btn_strip,
            text=next_btn_text,
            height=42,
            corner_radius=8,
            fg_color=next_btn_color,
            hover_color=hover_color,
            text_color="#FFFFFF",
            font=ctk.CTkFont(weight="bold"),
            command=self._handle_advance_wizard_step
        )

        btn_next.pack(
            side="right",
            padx=(10, 0),
            expand=True,
            fill="x"
        )

        # BACK BUTTON
        if self.current_idx > 0:
            btn_prev = ctk.CTkButton(
                btn_strip,
                text="⬅️ Back",
                height=42,
                corner_radius=8,
                fg_color="transparent",
                border_color="#A1A1AA",
                border_width=1,
                text_color="#FFFFFF",
                command=self._handle_regress_wizard_step
            )

            btn_prev.pack(
                side="left",
                padx=(0, 10),
                expand=True,
                fill="x"
            )

    # ------------------------------------------------------------------
    # WIZARD NAVIGATION
    # ------------------------------------------------------------------

    def _handle_advance_wizard_step(self):
        """
        Validates the current exercise duration.

        On the final exercise, this calls the database commit method.
        """

        raw_time = self.entry_step_time.get().strip()

        try:
            mins = int(raw_time)

            if mins <= 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Validation Error",
                "Please provide a valid whole number greater than 0."
            )
            return

        # Store this exercise's duration
        self.exercise_durations[self.current_idx] = mins

        # Recalculate total instead of continually adding.
        # This prevents double-counting if the user goes Back.
        self.accumulated_duration_mins = sum(
            self.exercise_durations.values()
        )

        # More exercises remain
        if self.current_idx < len(self.exercises) - 1:
            self.current_idx += 1
            self.render_active_step_wizard()
            return

        # Final exercise
        self._execute_commit_completed_session_to_db()

    def _handle_regress_wizard_step(self):
        """Moves back to the previous exercise."""

        if self.current_idx > 0:

            # Save the current input before going backwards
            raw_time = self.entry_step_time.get().strip()

            try:
                mins = int(raw_time)

                if mins > 0:
                    self.exercise_durations[self.current_idx] = mins

            except ValueError:
                pass

            self.current_idx -= 1

            # Recalculate total
            self.accumulated_duration_mins = sum(
                self.exercise_durations.values()
            )

            self.render_active_step_wizard()

    # ------------------------------------------------------------------
    # SAVE COMPLETED WORKOUT
    # ------------------------------------------------------------------

    def _execute_commit_completed_session_to_db(self):
        """
        Calculates calories and saves the completed workout
        to the activities database table.
        """

        # Make sure the final exercise duration is included.
        raw_time = self.entry_step_time.get().strip()

        try:
            final_mins = int(raw_time)

            if final_mins <= 0:
                raise ValueError

            self.exercise_durations[self.current_idx] = final_mins

        except ValueError:
            messagebox.showerror(
                "Validation Error",
                "Please provide a valid whole number greater than 0."
            )
            return

        # Calculate total duration from all exercises.
        self.accumulated_duration_mins = sum(
            self.exercise_durations.values()
        )

        if self.accumulated_duration_mins <= 0:
            messagebox.showerror(
                "Workout Error",
                "Workout duration must be greater than zero."
            )
            return

        today_str = datetime.now().strftime("%Y-%m-%d")

        # --------------------------------------------------------------
        # Get user's weight
        # --------------------------------------------------------------

        weight_kg = 70.0

        try:
            prof = self.db.execute_read(
                "SELECT weight_kg FROM user_profile LIMIT 1"
            )

            if prof and prof[0]["weight_kg"]:
                weight_kg = float(prof[0]["weight_kg"])

        except Exception:
            # Keep the default weight if the profile cannot be read.
            weight_kg = 70.0

        # --------------------------------------------------------------
        # Calculate calories
        # --------------------------------------------------------------

        try:
            calories = CalorieCalculator.calculate(
                "Custom Routine",
                self.accumulated_duration_mins,
                weight_kg
            )

        except Exception as e:
            messagebox.showerror(
                "Calculation Error",
                f"Failed to calculate calories:\n{e}"
            )
            return

        # --------------------------------------------------------------
        # Insert completed workout into database
        # --------------------------------------------------------------

        query = """
            INSERT INTO activities (
                activity_type,
                duration_minutes,
                distance_km,
                steps,
                calories_burned,
                log_date,
                notes
            )
            VALUES (?, ?, 0, 0, ?, ?, ?)
        """

        routine_name = self.active_routine["name"]

        notes = (
            f"Completed pre-made routine plan tracking: "
            f"{routine_name}"
        )

        activity_type = f"Routine: {routine_name}"

        try:
            self.db.execute_write(
                query,
                (
                    activity_type,
                    self.accumulated_duration_mins,
                    calories,
                    today_str,
                    notes
                )
            )

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                f"Failed to register completed workout:\n{e}"
            )
            return

        # --------------------------------------------------------------
        # Success message
        # --------------------------------------------------------------

        messagebox.showinfo(
            "Workout Complete!",
            (
                f"Congratulations!\n\n"
                f"Routine: {routine_name}\n"
                f"Exercises: {len(self.exercises)}\n"
                f"Total active time: "
                f"{self.accumulated_duration_mins} minutes\n"
                f"Calories burned: {calories:.0f}\n\n"
                f"Session saved to history!"
            )
        )

        # Reset workout state
        self.active_routine = None
        self.exercises = []
        self.current_idx = 0
        self.accumulated_duration_mins = 0
        self.exercise_durations = {}

        # Return to routine selection
        self.render_routine_selector_screen()

    # ------------------------------------------------------------------
    # VIEW CLEANUP
    # ------------------------------------------------------------------

    def _clear_view_canvas(self):
        """Destroys all widgets currently displayed in this frame."""

        for widget in self.winfo_children():
            widget.destroy()