import tkinter as tk
import time
import winsound
import threading
import psutil
import sys
import math
from pystray import MenuItem as item, Icon
from PIL import Image, ImageDraw, ImageFont


class TimerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()

        # Инициализация параметров
        self.timer_running = True
        self.paused = False
        self.accumulated_time = 0
        self.last_check = time.time()
        self.check_interval = 60  # Проверка каждые 60 секунд
        self.target_time = 5400  # 1.5 часа = 5400 секунд  !!!!!!!!!!!!
        self.sound_playing = False

        # Проверка времени загрузки системы
        if time.time() - psutil.boot_time() < 300:
            self.accumulated_time = 0

        # Настройка стилей
        self.button_font = ('Arial', 12, 'bold')
        self.title_font = ('Arial', 16, 'bold')
        # Установка фона окна
        self.bg_color = '#6A5ACD'  # Сиреневый
        # Установка цвета текста
        self.fg_color = '#F0F8FF'  # Белый
        self.btn_colors = {
            'green': ('#4CAF50', '#45A049'),
            'red': ('#F44336', '#D32F2F')
        }

        # Иконка в системном трее
        self.create_tray_icon()

        self.timer_thread = threading.Thread(target=self.run_timer, daemon=True)
        self.timer_thread.start()
        self.root.mainloop()

    def create_tray_icon(self):
        # Создание изображения секундомера
        image_size = 64
        image = Image.new('RGBA', (image_size, image_size), (0, 0, 0, 0))
        dc = ImageDraw.Draw(image)

        # Основной круг
        dc.ellipse([(12, 12), (52, 52)], fill=self.bg_color, outline='white', width=2)

        # Стрелка
        center = (32, 32)
        dc.line([center, (32, 16)], fill='white', width=3, joint='curve')

        # Кнопка сверху
        dc.rectangle([(28, 8), (36, 12)], fill='white')

        # Цифры
        font = ImageFont.truetype("arial.ttf", 12)
        for i, angle in enumerate(range(0, 360, 90)):
            x = 32 + int(25 * math.cos(math.radians(angle)))
            y = 32 + int(25 * math.sin(math.radians(angle)))
            dc.text((x - 3, y - 5), str(i * 3), fill='white', font=font)

        menu = (
            item('Продлить на 30 мин', self.add_30min),
            item('Пауза/Старт', self.toggle_pause),
            item('Выход', self.exit_app)
        )

        self.icon = Icon("break_timer", image, "Таймер перерывов", menu)
        threading.Thread(target=self.icon.run, daemon=True).start()

    def run_timer(self):
        while self.timer_running:
            if not self.paused:
                current_time = time.time()
                elapsed = current_time - self.last_check

                if elapsed <= self.check_interval + 10:
                    self.accumulated_time += elapsed
                else:
                    print("Обнаружен период сна")

                self.last_check = current_time

                if self.accumulated_time >= self.target_time:
                    self.show_alert()
                    self.accumulated_time = 0

            time.sleep(self.check_interval)

    def show_alert(self):
        self.alert_window = tk.Toplevel()
        self.alert_window.overrideredirect(True)  # Убираем стандартный заголовок

        # Создаем кастомный заголовок
        title_bar = tk.Frame(self.alert_window, bg='#4B0082', relief='raised', bd=0)
        title_bar.pack(fill='x')

        # Заголовок
        title_label = tk.Label(
            title_bar,
            text="Перерыв!",
            bg='#4B0082',  # Фон заголовка
            fg=self.fg_color,  # Белый текст
            font=('Arial', 14, 'bold')
        )
        title_label.pack(side='left', padx=10)

        # Кнопка закрытия
        close_button = tk.Button(
            title_bar,
            text='×',
            bg='#4B0082',  # Фон кнопки
            fg=self.fg_color,  # Белый текст
            bd=0,
            font=('Arial', 14, 'bold'),
            command=self.alert_window.destroy
        )
        close_button.pack(side='right', padx=10)

        # Основное содержимое окна
        content_frame = tk.Frame(self.alert_window, bg=self.bg_color)  # Фон основного окна
        content_frame.pack(fill='both', expand=True)

        # Позиционирование окна
        screen_width = self.alert_window.winfo_screenwidth()
        screen_height = self.alert_window.winfo_screenheight()
        window_width = 500
        window_height = 220
        x = (screen_width - window_width) // 2
        y = int(screen_height * 0.66) - window_height // 2
        self.alert_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Заголовок основного окна
        tk.Label(
            content_frame,
            text="Вы работали 1,5 часа\nНадо сделать перерыв!",
            font=self.title_font,
            bg=self.bg_color,  # Фон основного окна
            fg=self.fg_color,  # Белый текст
            pady=20
        ).pack()

        # Кнопки
        btn_frame = tk.Frame(content_frame, bg=self.bg_color)
        btn_frame.pack(pady=15)

        # Зеленая кнопка
        tk.Button(
            btn_frame,
            text="Перезапуск",
            font=self.button_font,
            bg=self.btn_colors['green'][0],
            fg=self.fg_color,  # Белый текст
            activebackground=self.btn_colors['green'][1],
            relief='flat',
            padx=20,
            pady=10,
            command=self.restart_timer
        ).pack(side=tk.LEFT, padx=15)

        # Красная кнопка
        tk.Button(
            btn_frame,
            text="Остановить таймер",
            font=self.button_font,
            bg=self.btn_colors['red'][0],
            fg=self.fg_color,  # Белый текст
            activebackground=self.btn_colors['red'][1],
            relief='flat',
            padx=20,
            pady=10,
            command=self.disable_timer
        ).pack(side=tk.RIGHT, padx=15)

        # Звуковое оповещение
        threading.Thread(target=self.play_sound, daemon=True).start()

    def play_sound(self):
        try:
            winsound.PlaySound('dopamin-short.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception as e:
            print(f"Ошибка звука: {e}")

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

    def add_30min(self):
        self.accumulated_time -= 1800
        self.accumulated_time = max(self.accumulated_time, 0)

    def toggle_pause(self):
        self.paused = not self.paused
        if not self.paused:
            self.last_check = time.time()

    def exit_app(self):
        self.disable_timer()
        self.icon.stop()


if __name__ == "__main__":
    app = TimerApp()