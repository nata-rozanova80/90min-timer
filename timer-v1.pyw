import sys
import tkinter as tk
import time
import winsound
import threading
import logging
import datetime
import os


class TimerApp:
    def __init__(self):
        self.start_time = datetime.datetime.now()  # Время старта программы
        self.timer_triggers = 0  # Счётчик срабатываний
        self.last_trigger_time = None  # Время последнего срабатывания

        logging.basicConfig(filename='timer.log', level=logging.INFO)
        logging.info("=" * 50)
        logging.info(f"New timer-v1 start at {self.start_time}")
        logging.info("App timer-v1 is running")

        logging.info(f"Python version (timer-v1): {sys.version}")
        logging.info(f"Path (timer-v1): {os.path.abspath(__file__)}")

        self.root = tk.Tk()
        self.root.withdraw()

        self.timer_running = True
        self.accumulated_time = 0
        self.last_check = time.time()
        self.check_interval = 60  # Тестовый интервал (60 сек)
        self.target_time = 5400  # Для теста (замените на 5400)
        self.sound_playing = False

        # Настройки шрифта
        self.button_font = ('Arial', 12, 'bold')

        self.timer_thread = threading.Thread(target=self.run_timer, daemon=True)
        self.timer_thread.start()
        self.root.mainloop()

    def run_timer(self):
        while self.timer_running:
            current_time = time.time()
            elapsed = current_time - self.last_check

            if elapsed <= self.check_interval + 10:
                self.accumulated_time += elapsed
            else:
                print("Обнаружен период сна")

            self.last_check = current_time

            # Лог 1: Общее время работы
            total_time = datetime.datetime.now() - self.start_time
            logging.info(f"Total active time: {total_time}")  # NEW LOG <button class="citation-flag" data-index="1">

            if self.accumulated_time >= self.target_time:
                self.show_alert()
                self.accumulated_time = 0

            time.sleep(self.check_interval)

    def show_alert(self):
        self.timer_triggers += 1  # Увеличение счётчика
        self.last_trigger_time = datetime.datetime.now()  # Обновление времени

        self.alert_window = tk.Toplevel()
        self.alert_window.title("Перерыв!")
        self.alert_window.configure(bg='#F0F0F0')

        # Позиционирование окна
        screen_width = self.alert_window.winfo_screenwidth()
        screen_height = self.alert_window.winfo_screenheight()
        window_width = 450
        window_height = 200
        x = (screen_width - window_width) // 2
        y = int(screen_height * 0.66) - window_height // 2
        self.alert_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Лог 2 и 3
        #logging.info(f"The alert went off {self.timer_triggers} times <button class="citation-flag" data-index="2">")  # NEW LOG
        logging.info(
            f'The alert went off {self.timer_triggers} times <button class="citation-flag" data-index="2">')  # NEW LOG <button class="citation-flag" data-index="1">
        if self.last_trigger_time:
            time_since_last = datetime.datetime.now() - self.last_trigger_time
            logging.info(f"Time since last alert: {time_since_last}")  # NEW LOG <button class="citation-flag" data-index="3">

        # Воспроизведение звука
        self.sound_playing = True
        threading.Thread(target=self.play_sound, daemon=True).start()

        # Основное содержимое
        tk.Label(self.alert_window,
                 text="Вы работали 1,5 часа\nНадо сделать перерыв!",
                 font=('Arial', 14, 'bold'),
                 bg='#F0F0F0',
                 pady=20).pack()

        btn_frame = tk.Frame(self.alert_window, bg='#F0F0F0')
        btn_frame.pack(pady=15)

        # Зеленая кнопка
        btn_restart = tk.Button(btn_frame,
                                text="Пауза/Перезапуск",
                                font=self.button_font,
                                bg='#4CAF50',
                                fg='white',
                                activebackground='#45A049',
                                activeforeground='white',
                                relief='flat',
                                padx=20,
                                pady=10,
                                command=self.restart_timer)
        btn_restart.pack(side=tk.LEFT, padx=15)

        # Красная кнопка
        btn_disable = tk.Button(btn_frame,
                                text="Отключить таймер",
                                font=self.button_font,
                                bg='#F44336',
                                fg='white',
                                activebackground='#D32F2F',
                                activeforeground='white',
                                relief='flat',
                                padx=20,
                                pady=10,
                                command=self.disable_timer)
        btn_disable.pack(side=tk.RIGHT, padx=15)

    def play_sound(self):
        try:
            winsound.PlaySound('dopamin-short.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception as e:
            print(f"Ошибка звука: {e}")
        self.sound_playing = False

    def stop_sound(self):
        winsound.PlaySound(None, winsound.SND_FILENAME)

    def restart_timer(self):
        self.stop_sound()
        self.accumulated_time = 0
        self.alert_window.destroy()

    def disable_timer(self):
        self.stop_sound()
        self.timer_running = False
        self.alert_window.destroy()
        self.root.destroy()


if __name__ == "__main__":
    app = TimerApp()