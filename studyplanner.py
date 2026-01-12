import json
import os
import threading
import time
from datetime import datetime, time as dt_time

import pytz
import schedule
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import IconRightWidget, TwoLineAvatarIconListItem
from kivymd.uix.pickers import MDDatePicker, MDTimePicker

from messaging_service import send_study_reminder

# --- Set the application window size for a mobile-like experience ---
Window.size = (350, 600)

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivymd.app import MDApp

Builder.load_file("studyplanner.kv")

# --- Classes for Dialog Content ---
class ScheduledDialogContent(MDBoxLayout):
    pass


class DailyPlanDialogContent(MDBoxLayout):
    pass


class StudyPlannerScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.scheduled_tasks = []
        self.scheduled_dialog = None
        self.daily_tasks = []
        self.daily_dialog = None 


    def on_enter(self):
        # --- Data Files ---
        self.scheduled_tasks_file = "study_plan.json"
        self.daily_plan_file = "daily_plan.json"

        self.scheduled_tasks = self.load_data(self.scheduled_tasks_file)
        self.daily_plan_entries = self.load_data(self.daily_plan_file)

        # --- State Variables ---
        self.scheduler_thread_running = True
        self.last_daily_trigger = None

        # UI lists from kv file
        self.scheduled_task_list = self.ids.scheduled_task_list
        self.daily_plan_list = self.ids.daily_plan_list

        Clock.schedule_once(self.refresh_scheduled_list)
        Clock.schedule_once(self.refresh_daily_plan_list)
        self.start_scheduler_thread()


    def on_leave(self):
        self.scheduler_thread_running = False

    # --- Generic Data Persistence ---
    def load_data(self, file_path):
        if not os.path.exists(file_path):
            return []
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_data(self, data, file_path):
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

    # --- Scheduled Sessions ---
    def show_add_scheduled_dialog(self):
        if self.scheduled_dialog:
            self.scheduled_dialog.dismiss()
        if not self.scheduled_dialog:
            self.scheduled_dialog = MDDialog(
                title="Add Scheduled Task",
                type="custom",
                content_cls=ScheduledDialogContent(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        on_release=lambda x: self.scheduled_dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="NEXT",
                        on_release=self.process_scheduled_dialog_data
                    ),
                ],
            )
        self.scheduled_dialog.open()

    def process_scheduled_dialog_data(self, *args):
        self.temp_scheduled_subject = self.scheduled_dialog.content_cls.ids.subject_field.text.strip()
        self.temp_scheduled_topic = self.scheduled_dialog.content_cls.ids.topic_field.text.strip()
        if not self.temp_scheduled_subject or not self.temp_scheduled_topic:
            return
        self.scheduled_dialog.dismiss()
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_date_save)
        date_dialog.open()

    def on_date_save(self, instance, value, date_range):
        self.selected_date = value
        time_dialog = MDTimePicker()
        time_dialog.bind(on_save=self.on_scheduled_time_save)
        time_dialog.open()

    def on_scheduled_time_save(self, instance, value):
        task_datetime = datetime.combine(self.selected_date, value)
        new_task = {
            "id": int(time.time()),
            "subject": self.temp_scheduled_subject,
            "topic": self.temp_scheduled_topic,
            "datetime_iso": task_datetime.isoformat(),
        }
        self.scheduled_tasks.append(new_task)
        self.save_data(self.scheduled_tasks, self.scheduled_tasks_file)
        self.refresh_scheduled_list()

    def delete_scheduled_task(self, task_id):
        self.scheduled_tasks = [t for t in self.scheduled_tasks if t["id"] != task_id]
        self.save_data(self.scheduled_tasks, self.scheduled_tasks_file)
        self.refresh_scheduled_list()

    def refresh_scheduled_list(self, *args):
        self.scheduled_task_list.clear_widgets()
        sorted_tasks = sorted(self.scheduled_tasks, key=lambda x: x["datetime_iso"])
        for task in sorted_tasks:
            task_dt = datetime.fromisoformat(task["datetime_iso"])
            display_time = task_dt.strftime("%a, %d %b %Y at %I:%M %p")
            list_item = TwoLineAvatarIconListItem(
                text=f"[b]{task['subject']}[/b]",
                secondary_text=f"{task['topic']} on {display_time}",
            )
            delete_icon = IconRightWidget(
                icon="delete-outline",
                on_release=lambda x, t_id=task["id"]: self.delete_scheduled_task(t_id),
            )
            list_item.add_widget(delete_icon)
            self.scheduled_task_list.add_widget(list_item)

    # --- Daily Plan ---
    def show_add_daily_plan_dialog(self):
        if self.daily_dialog:
            self.daily_dialog.dismiss()
        if not self.daily_dialog:
            self.daily_dialog = MDDialog(
                title="Add Daily Plan",
                type="custom",
                content_cls=DailyPlanDialogContent(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        on_release=lambda x: self.daily_dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="NEXT",
                        on_release=self.process_daily_plan_dialog_data
                    ),
                ],
            )
        self.daily_dialog.open()

    def process_daily_plan_dialog_data(self, *args):
        self.temp_daily_subject = self.daily_dialog.content_cls.ids.subject_field.text.strip()
        self.temp_daily_topic = self.daily_dialog.content_cls.ids.topic_field.text.strip()
        if not self.temp_daily_subject:
            return
        self.daily_dialog.dismiss()
        time_dialog = MDTimePicker()
        time_dialog.bind(on_save=self.on_daily_plan_time_save)
        time_dialog.open()

    def on_daily_plan_time_save(self, instance, value):
        new_entry = {
            "id": int(time.time()),
            "time": value.strftime("%H:%M"),
            "subject": self.temp_daily_subject,
            "topic": self.temp_daily_topic,
        }
        self.daily_plan_entries.append(new_entry)
        self.save_data(self.daily_plan_entries, self.daily_plan_file)
        self.refresh_daily_plan_list()

    def delete_daily_plan_entry(self, entry_id):
        self.daily_plan_entries = [e for e in self.daily_plan_entries if e["id"] != entry_id]
        self.save_data(self.daily_plan_entries, self.daily_plan_file)
        self.refresh_daily_plan_list()

    def refresh_daily_plan_list(self, *args):
        self.daily_plan_list.clear_widgets()
        sorted_entries = sorted(self.daily_plan_entries, key=lambda x: x["time"])
        for entry in sorted_entries:
            entry_time = dt_time.fromisoformat(entry["time"]).strftime("%I:%M %p")
            secondary_text = f"{entry['topic']}" if entry["topic"] else "Daily Study Session"
            list_item = TwoLineAvatarIconListItem(
                text=f"{entry['subject']} at {entry_time}",
                secondary_text=secondary_text,
            )
            delete_icon = IconRightWidget(
                icon="delete-outline",
                on_release=lambda x, e_id=entry["id"]: self.delete_daily_plan_entry(e_id),
            )
            list_item.add_widget(delete_icon)
            self.daily_plan_list.add_widget(list_item)

    # --- Background Scheduler ---
    def start_scheduler_thread(self):
        thread = threading.Thread(target=self.run_scheduler, daemon=True)
        thread.start()

    def run_scheduler(self):
        schedule.every(30).seconds.do(self.check_schedules)
        while self.scheduler_thread_running:
            schedule.run_pending()
            time.sleep(1)

    def trigger_reminder(self, subject, topic):
        print(f"Reminder: Time for {subject} - {topic}")

        # Send SMS
        try:
            send_study_reminder(subject, topic)
        except Exception as e:
            print(f"Error sending SMS reminder: {e}")

    def check_schedules(self):
        ist = pytz.timezone("Asia/Kolkata")
        now_ist = datetime.now(ist)

        # --- One-time scheduled tasks ---
        tasks_to_remove = []
        for task in self.scheduled_tasks:
            task_dt_naive = datetime.fromisoformat(task["datetime_iso"])
            task_dt_ist = ist.localize(task_dt_naive)
            if now_ist >= task_dt_ist:
                self.trigger_reminder(task["subject"], task["topic"])
                tasks_to_remove.append(task["id"])

        if tasks_to_remove:
            self.scheduled_tasks = [t for t in self.scheduled_tasks if t["id"] not in tasks_to_remove]
            self.save_data(self.scheduled_tasks, self.scheduled_tasks_file)
            Clock.schedule_once(self.refresh_scheduled_list)

        # --- Daily plan repeating entries ---
        current_time_str = now_ist.strftime("%H:%M")
        if self.last_daily_trigger == current_time_str:
            return

        for entry in self.daily_plan_entries:
            if entry["time"] == current_time_str:
                self.trigger_reminder(entry["subject"], entry["topic"])
                self.last_daily_trigger = current_time_str
                break