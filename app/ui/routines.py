import customtkinter as ctk
from tkinter import messagebox

from app.database.database import DatabaseManager


class RoutinesView(ctk.CTkFrame):
    """
    Manages structured workout routines.

    Allows users to:
    - Create workout routine containers
    - Add exercises to routines
    - Set duration/repetition targets
    - View routines and their exercises
    - Delete complete routines and their exercises
    """

    def __init__(self, parent, controller):
        super().__init__(
            parent,
            fg_color="#1A1A1A",
            corner_radius=0
        )

        self.controller = controller
        self.db = DatabaseManager()

        # Main layout
        self.grid_columnconfigure(0, weight=4)
        self.grid_columnconfigure(1, weight=5)
        self.grid_rowconfigure(0, weight=1)

        self._build_composition_control_panel()
        self._build_overview_display_panel()
        self.reload_routines_context()

    # ================================================================
    # LEFT PANEL
    # ================================================================

    def _build_composition_control_panel(self):
        """Builds routine creation and exercise addition controls."""

        self.left_scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )

        self.left_scroll.grid(
            row=0,
            column=0,
            padx=(30, 15),
            pady=20,
            sticky="nsew"
        )

        # ------------------------------------------------------------
        # CREATE ROUTINE
        # ------------------------------------------------------------

        box_container = ctk.CTkFrame(
            self.left_scroll,
            fg_color="#2E2E2E",
            corner_radius=12
        )

        box_container.pack(
            fill="x",
            pady=(0, 15)
        )

        lbl_sec1 = ctk.CTkLabel(
            box_container,
            text="✨ Create New Routine Shell",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            ),
            text_color="#FFFFFF"
        )

        lbl_sec1.pack(
            anchor="w",
            padx=20,
            pady=(20, 12)
        )

        lbl_name = ctk.CTkLabel(
            box_container,
            text="Routine Name *",
            font=ctk.CTkFont(size=12),
            text_color="#A1A1AA"
        )

        lbl_name.pack(
            anchor="w",
            padx=20,
            pady=(2, 2)
        )

        self.entry_rname = ctk.CTkEntry(
            box_container,
            placeholder_text="e.g. Morning Cardio, Leg Day",
            height=35,
            fg_color="#1A1A1A",
            border_color="#A1A1AA"
        )

        self.entry_rname.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )

        btn_make_r = ctk.CTkButton(
            box_container,
            text="🏗️ Initialize Routine Shell",
            height=38,
            corner_radius=8,
            fg_color="#0EA5E9",
            hover_color="#0284C7",
            text_color="#FFFFFF",
            font=ctk.CTkFont(weight="bold"),
            command=self._handle_routine_creation
        )

        btn_make_r.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        # ------------------------------------------------------------
        # ADD EXERCISE
        # ------------------------------------------------------------

        box_exercises = ctk.CTkFrame(
            self.left_scroll,
            fg_color="#2E2E2E",
            corner_radius=12
        )

        box_exercises.pack(
            fill="x",
            pady=10
        )

        lbl_sec2 = ctk.CTkLabel(
            box_exercises,
            text="🏋️‍♂️ Append Exercise to Routine",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            ),
            text_color="#FFFFFF"
        )

        lbl_sec2.pack(
            anchor="w",
            padx=20,
            pady=(20, 12)
        )

        # Target routine
        lbl_target = ctk.CTkLabel(
            box_exercises,
            text="Select Target Routine Container *",
            font=ctk.CTkFont(size=12),
            text_color="#A1A1AA"
        )

        lbl_target.pack(
            anchor="w",
            padx=20,
            pady=(2, 2)
        )

        self.combo_target_routine = ctk.CTkComboBox(
            box_exercises,
            values=[],
            height=35,
            fg_color="#1A1A1A",
            border_color="#A1A1AA"
        )

        self.combo_target_routine.pack(
            fill="x",
            padx=20,
            pady=(0, 12)
        )

        # Exercise name
        lbl_ex_name = ctk.CTkLabel(
            box_exercises,
            text="Exercise Name *",
            font=ctk.CTkFont(size=12),
            text_color="#A1A1AA"
        )

        lbl_ex_name.pack(
            anchor="w",
            padx=20,
            pady=(2, 2)
        )

        self.combo_ex_name = ctk.CTkComboBox(
            box_exercises,
            values=[
                "Jumping Jacks",
                "Skipping",
                "Jogging",
                "Squats",
                "Plank",
                "Push-ups",
                "Sit-ups",
                "Stretching",
                "Lunges",
                "Burpees"
            ],
            height=35,
            fg_color="#1A1A1A",
            border_color="#A1A1AA"
        )

        self.combo_ex_name.pack(
            fill="x",
            padx=20,
            pady=(0, 12)
        )

        # Targets
        targets_frame = ctk.CTkFrame(
            box_exercises,
            fg_color="transparent"
        )

        targets_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )

        targets_frame.grid_columnconfigure(
            0,
            weight=1
        )

        targets_frame.grid_columnconfigure(
            1,
            weight=1
        )

        lbl_dur = ctk.CTkLabel(
            targets_frame,
            text="Duration (seconds)",
            font=ctk.CTkFont(size=12),
            text_color="#A1A1AA"
        )

        lbl_dur.grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 5)
        )

        self.entry_ex_dur = ctk.CTkEntry(
            targets_frame,
            placeholder_text="e.g. 60 (or 0)",
            height=35,
            fg_color="#1A1A1A",
            border_color="#A1A1AA"
        )

        self.entry_ex_dur.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(0, 5)
        )

        lbl_reps = ctk.CTkLabel(
            targets_frame,
            text="Reps Target",
            font=ctk.CTkFont(size=12),
            text_color="#A1A1AA"
        )

        lbl_reps.grid(
            row=0,
            column=1,
            sticky="w",
            padx=(5, 0)
        )

        self.entry_ex_reps = ctk.CTkEntry(
            targets_frame,
            placeholder_text="e.g. 20 (or 0)",
            height=35,
            fg_color="#1A1A1A",
            border_color="#A1A1AA"
        )

        self.entry_ex_reps.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=(5, 0)
        )

        btn_add_ex = ctk.CTkButton(
            box_exercises,
            text="➕ Add Exercise Item",
            height=38,
            corner_radius=8,
            fg_color="#22C55E",
            hover_color="#16A34A",
            text_color="#FFFFFF",
            font=ctk.CTkFont(weight="bold"),
            command=self._handle_exercise_addition
        )

        btn_add_ex.pack(
            fill="x",
            padx=20,
            pady=(5, 20)
        )

    # ================================================================
    # RIGHT PANEL
    # ================================================================

    def _build_overview_display_panel(self):
        """Builds the routine overview panel."""

        self.right_container = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.right_container.grid(
            row=0,
            column=1,
            padx=(15, 30),
            pady=20,
            sticky="nsew"
        )

        self.right_container.grid_columnconfigure(
            0,
            weight=1
        )

        self.right_container.grid_rowconfigure(
            1,
            weight=1
        )

        lbl_title = ctk.CTkLabel(
            self.right_container,
            text="My Reusable Routine Blueprints",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            ),
            text_color="#FFFFFF"
        )

        lbl_title.grid(
            row=0,
            column=0,
            padx=5,
            pady=(0, 15),
            sticky="w"
        )

        self.scroll_routines = ctk.CTkScrollableFrame(
            self.right_container,
            fg_color="#2E2E2E",
            corner_radius=12
        )

        self.scroll_routines.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

    # ================================================================
    # CREATE ROUTINE
    # ================================================================

    def _handle_routine_creation(self):
        """Creates a new routine container."""

        name = self.entry_rname.get().strip()

        if not name:
            messagebox.showerror(
                "Validation Error",
                "Routine Name field cannot be left blank."
            )
            return

        try:
            self.db.execute_write(
                "INSERT INTO routines (name) VALUES (?)",
                (name,)
            )

            messagebox.showinfo(
                "Success",
                f"Routine shell '{name}' successfully created!"
            )

            self.entry_rname.delete(
                0,
                "end"
            )

            self.reload_routines_context()

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                f"Could not create routine '{name}'.\n\n{e}"
            )

    # ================================================================
    # ADD EXERCISE
    # ================================================================

    def _handle_exercise_addition(self):
        """Adds an exercise to the selected routine."""

        target_routine_name = (
            self.combo_target_routine.get().strip()
        )

        exercise_name = (
            self.combo_ex_name.get().strip()
        )

        raw_dur = (
            self.entry_ex_dur.get().strip()
            or "0"
        )

        raw_reps = (
            self.entry_ex_reps.get().strip()
            or "0"
        )

        if not target_routine_name:
            messagebox.showerror(
                "Validation Error",
                "You must select a target routine container first."
            )
            return

        if not exercise_name:
            messagebox.showerror(
                "Validation Error",
                "Please select or enter an exercise name."
            )
            return

        try:
            duration = int(raw_dur)
            reps = int(raw_reps)

            if duration < 0 or reps < 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Validation Error",
                "Duration and reps must be valid non-negative numbers."
            )
            return

        try:
            routine_row = self.db.execute_read(
                "SELECT id FROM routines WHERE name = ?",
                (target_routine_name,)
            )

            if not routine_row:
                messagebox.showerror(
                    "Routine Error",
                    "The selected routine could not be found."
                )
                return

            routine_id = routine_row[0]["id"]

            count_row = self.db.execute_read(
                """
                SELECT COUNT(*) AS total
                FROM routine_exercises
                WHERE routine_id = ?
                """,
                (routine_id,)
            )

            next_idx = count_row[0]["total"] + 1

            self.db.execute_write(
                """
                INSERT INTO routine_exercises (
                    routine_id,
                    exercise_name,
                    order_index,
                    target_duration_seconds,
                    target_reps
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    routine_id,
                    exercise_name,
                    next_idx,
                    duration,
                    reps
                )
            )

            messagebox.showinfo(
                "Success",
                f"Appended '{exercise_name}' to '{target_routine_name}'!"
            )

            self.entry_ex_dur.delete(
                0,
                "end"
            )

            self.entry_ex_reps.delete(
                0,
                "end"
            )

            self.reload_routines_context()

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                f"Failed to map exercise configuration:\n{e}"
            )

    # ================================================================
    # REFRESH ROUTINES
    # ================================================================

    def reload_routines_context(self):
        """Reloads the routine dropdown and visual routine cards."""

        # ------------------------------------------------------------
        # Refresh dropdown
        # ------------------------------------------------------------

        try:
            routines_data = self.db.execute_read(
                "SELECT name FROM routines ORDER BY name ASC"
            )

            r_names = [
                row["name"]
                for row in routines_data
            ]

            self.combo_target_routine.configure(
                values=r_names
            )

            if r_names:
                current_selection = (
                    self.combo_target_routine.get().strip()
                )

                if current_selection not in r_names:
                    self.combo_target_routine.set(
                        r_names[0]
                    )

            else:
                self.combo_target_routine.set("")

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                f"Failed to load routines:\n{e}"
            )

        # ------------------------------------------------------------
        # Clear existing cards
        # ------------------------------------------------------------

        for widget in self.scroll_routines.winfo_children():
            widget.destroy()

        # ------------------------------------------------------------
        # Get all routines
        # ------------------------------------------------------------

        try:
            all_routines = self.db.execute_read(
                "SELECT * FROM routines ORDER BY id DESC"
            )

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                f"Failed to load routine overview:\n{e}"
            )
            return

        # ------------------------------------------------------------
        # No routines
        # ------------------------------------------------------------

        if not all_routines:
            empty_lbl = ctk.CTkLabel(
                self.scroll_routines,
                text=(
                    "No workout routines compiled yet.\n"
                    "Use the left layout tools to initialize blueprints!"
                ),
                text_color="#A1A1AA"
            )

            empty_lbl.pack(
                pady=100
            )

            return

        # ------------------------------------------------------------
        # Build routine cards
        # ------------------------------------------------------------

        for r_row in all_routines:

            routine_id = r_row["id"]
            routine_name = r_row["name"]

            r_card = ctk.CTkFrame(
                self.scroll_routines,
                fg_color="#1A1A1A",
                corner_radius=8
            )

            r_card.pack(
                fill="x",
                padx=15,
                pady=8
            )

            # --------------------------------------------------------
            # Header
            # --------------------------------------------------------

            header_strip = ctk.CTkFrame(
                r_card,
                fg_color="transparent"
            )

            header_strip.pack(
                fill="x",
                padx=15,
                pady=(12, 8)
            )

            lbl_r_title = ctk.CTkLabel(
                header_strip,
                text=routine_name,
                font=ctk.CTkFont(
                    size=14,
                    weight="bold"
                ),
                text_color="#FFFFFF"
            )

            lbl_r_title.pack(
                side="left"
            )

            # --------------------------------------------------------
            # DELETE BUTTON
            # --------------------------------------------------------

            btn_del_r = ctk.CTkButton(
                header_strip,
                text="🗑️ Delete Routine",
                width=130,
                height=28,
                fg_color="#EF4444",
                hover_color="#DC2626",
                text_color="#FFFFFF",
                font=ctk.CTkFont(
                    size=11,
                    weight="bold"
                ),
                command=lambda rid=routine_id:
                    self._delete_entire_routine(rid)
            )

            btn_del_r.pack(
                side="right"
            )

            # --------------------------------------------------------
            # LOAD EXERCISES
            # --------------------------------------------------------

            try:
                ex_rows = self.db.execute_read(
                    """
                    SELECT *
                    FROM routine_exercises
                    WHERE routine_id = ?
                    ORDER BY order_index ASC
                    """,
                    (routine_id,)
                )

            except Exception as e:
                lbl_error = ctk.CTkLabel(
                    r_card,
                    text=f"Failed to load exercises: {e}",
                    text_color="#EF4444"
                )

                lbl_error.pack(
                    anchor="w",
                    padx=15,
                    pady=10
                )

                continue

            # --------------------------------------------------------
            # EMPTY ROUTINE
            # --------------------------------------------------------

            if not ex_rows:

                lbl_none = ctk.CTkLabel(
                    r_card,
                    text=(
                        "(No exercises appended to "
                        "this blueprint yet)"
                    ),
                    font=ctk.CTkFont(
                        size=11,
                        slant="italic"
                    ),
                    text_color="#A1A1AA"
                )

                lbl_none.pack(
                    anchor="w",
                    padx=15,
                    pady=(2, 10)
                )

            # --------------------------------------------------------
            # EXERCISES
            # --------------------------------------------------------

            else:

                for e_row in ex_rows:

                    ex_line = ctk.CTkFrame(
                        r_card,
                        fg_color="#2E2E2E",
                        corner_radius=4
                    )

                    ex_line.pack(
                        fill="x",
                        padx=20,
                        pady=3
                    )

                    details = (
                        f"{e_row['order_index']}. "
                        f"{e_row['exercise_name']}"
                    )

                    spec = []

                    # IMPORTANT:
                    # sqlite3.Row does NOT have .get()
                    duration = e_row["target_duration_seconds"]
                    reps = e_row["target_reps"]

                    if duration is not None and duration > 0:
                        spec.append(
                            f"⏱️ {duration}s"
                        )

                    if reps is not None and reps > 0:
                        spec.append(
                            f"🔢 {reps} reps"
                        )

                    if spec:
                        details_spec = (
                            f" — {', '.join(spec)}"
                        )
                    else:
                        details_spec = " — Standard Set"

                    lbl_ex = ctk.CTkLabel(
                        ex_line,
                        text=details + details_spec,
                        font=ctk.CTkFont(size=12),
                        text_color="#FFFFFF"
                    )

                    lbl_ex.pack(
                        side="left",
                        padx=10,
                        pady=5
                    )

    # ================================================================
    # DELETE ROUTINE
    # ================================================================

    def _delete_entire_routine(self, routine_id: int):
        """
        Deletes a routine and all exercises belonging to it.

        Child exercises are deleted first so this works even if
        ON DELETE CASCADE is not configured in SQLite.
        """

        # ------------------------------------------------------------
        # Find routine
        # ------------------------------------------------------------

        try:
            routine_rows = self.db.execute_read(
                "SELECT name FROM routines WHERE id = ?",
                (routine_id,)
            )

            if not routine_rows:
                messagebox.showerror(
                    "Delete Error",
                    "The selected routine no longer exists."
                )

                self.reload_routines_context()
                return

            routine_name = routine_rows[0]["name"]

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                f"Could not find the routine:\n{e}"
            )
            return

        # ------------------------------------------------------------
        # Ask for confirmation
        # ------------------------------------------------------------

        confirmed = messagebox.askyesno(
            "Confirm Delete",
            (
                f"Are you sure you want to permanently delete "
                f"the routine:\n\n"
                f"'{routine_name}'?\n\n"
                f"All exercises inside this routine will also "
                f"be deleted."
            )
        )

        if not confirmed:
            return

        # ------------------------------------------------------------
        # Delete routine
        # ------------------------------------------------------------

        try:
            # Delete child exercises first
            self.db.execute_write(
                """
                DELETE FROM routine_exercises
                WHERE routine_id = ?
                """,
                (routine_id,)
            )

            # Delete parent routine
            self.db.execute_write(
                """
                DELETE FROM routines
                WHERE id = ?
                """,
                (routine_id,)
            )

            # Refresh interface
            messagebox.showinfo(
                "Routine Deleted",
                f"'{routine_name}' was successfully deleted."
            )

            self.reload_routines_context()

        except Exception as e:
            messagebox.showerror(
                "Delete Error",
                f"Failed to delete routine:\n{e}"
            )
