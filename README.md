# Таймер для регулярных перерывов через 90 минут

Приложение для напоминания о перерывах каждые 1.5 часа работы за компьютером. 
Автоматически запускается при старте системы, работает в фоновом режиме.

![Пример окна уведомления](/Timer.jpg)


## Особенности

- 🕒 Автоматический подсчет активного времени работы
- 🔔 Звуковое уведомление и всплывающее окно
- 🖱️ Управление через интуитивные кнопки:
  - Перезапуск таймера
  - Полное отключение приложения
- 💤 Автоматическая пауза при простое системы
- 🎨 Кастомизируемый интерфейс

## Требования

- Python 3.7+
- Windows 10/11 (для Linux/macOS требуется модификация кода)
- Звуковая система

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/ваш-логин/90min-timer.git
cd 90min-timer
```

2. Поместите звуковой файл в формате WAV в папку проекта:
- Название файла: `dopamin-short.wav`
- Рекомендуемая длительность: 2-5 секунд

## Настройка

### Автозагрузка
**Для Windows:**
1. Создайте ярлык для `timer_app.pyw`
2. Поместите ярлык в папку автозагрузки:
   - `Win + R` → `shell:startup`

**Для Linux:**
```bash
sudo nano /etc/systemd/user/timer-app.service
```
Добавьте:
```ini
[Unit]
Description=90 Minute Timer

[Service]
ExecStart=/usr/bin/python3 /путь/к/проекту/timer_app.py

[Install]
WantedBy=default.target
```
Активируйте:
```bash
systemctl --user enable timer-app.service
```

## Модификация параметров

Для изменения интервалов отредактируйте в коде:
```python
self.check_interval = 60    # Частота проверок (сек)
self.target_time = 5400     # Время до срабатывания (1.5 часа)
```

## Компиляция в EXE (опционально)

1. Установите pyinstaller:
```bash
pip install pyinstaller
```

2. Соберите исполняемый файл:
```bash
pyinstaller --onefile --noconsole timer_app.py
```

## Лицензия

MIT License. Подробнее в файле [LICENSE](LICENSE).

---
**Важно:** При первом запуске разрешите приложению работать в фоновом режиме в настройках антивируса/брандмауэра.
```


