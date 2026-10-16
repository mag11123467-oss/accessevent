import tkinter as tk
from tkinter import ttk
import math
import os

# ==================== ДАННЫЕ ПЛАНЕТ ====================
# distance — в а.е. (1 а.е. = 149.6 млн км, Земля = 1.0)
# radius — в единицах радиуса Земли (Земля = 1.0)
# period — период обращения в годах (Земля = 1 год)
# color — цвет, если нет картинки

PLANETS = [
    {"name": "Меркурий", "distance": 0.4,  "radius": 0.38, "period": 0.241,  "color": "#a8a8a8"},
    {"name": "Венера",   "distance": 0.7,  "radius": 0.95, "period": 0.615,  "color": "#e6c98a"},
    {"name": "Земля",    "distance": 1.0,  "radius": 1.0,  "period": 1.0,    "color": "#3a80d2"},
    {"name": "Марс",     "distance": 1.5,  "radius": 0.53, "period": 1.881,  "color": "#c1440e"},
    {"name": "Юпитер",   "distance": 5.2,  "radius": 11.2, "period": 11.86,  "color": "#d8ca9d"},
    {"name": "Сатурн",   "distance": 9.5,  "radius": 9.5,  "period": 29.46,  "color": "#e3d9a8"},
    {"name": "Уран",     "distance": 19.0, "radius": 4.0,  "period": 84.01,  "color": "#afdbdb"},
    {"name": "Нептун",   "distance": 30.0, "radius": 3.9,  "period": 164.8,  "color": "#3f54ba"},
]

# ==================== ГЛАВНОЕ ОКНО ====================
root = tk.Tk()
root.title("Солнечная система — симуляция")
root.geometry("1200x800")
root.configure(bg="#000010")

# ==================== ХОЛСТ ====================
canvas = tk.Canvas(root, width=1200, height=700, bg="#000010", highlightthickness=0)
canvas.pack()

# ==================== СОСТОЯНИЕ ====================
state = {
    "zoom": 6.0,        # пикселей на 1 а.е. (будет масштабироваться ползунком)
    "speed": 1.0,       # множитель скорости
    "time": 0.0,        # прошло "лет"
    "running": True,
}

# Центр Солнца
CX, CY = 600, 350

# ==================== СОЛНЦЕ ====================
# Солнце = 109 радиусов Земли, но для отображения уменьшим
SUN_DISPLAY_R = 30

# ==================== РИСОВАНИЕ ====================
def draw_planet(x, y, r, color, name):
    """Рисует планету с подписью."""
    canvas.create_oval(x - r, y - r, x + r, y + r,
                       fill=color, outline="white", width=1)
    canvas.create_text(x, y - r - 8, text=name, fill="white",
                       font=("Arial", 8))


def draw_orbit(distance, zoom):
    """Рисует круг орбиты."""
    r = distance * zoom
    canvas.create_oval(CX - r, CY - r, CX + r, CY + r,
                       outline="#333355", width=1)


def draw():
    canvas.delete("all")

    zoom = state["zoom"]
    time_years = state["time"]

    # Солнце
    canvas.create_oval(CX - SUN_DISPLAY_R, CY - SUN_DISPLAY_R,
                       CX + SUN_DISPLAY_R, CY + SUN_DISPLAY_R,
                       fill="#ffcc00", outline="#ff8800", width=2)
    canvas.create_text(CX, CY + SUN_DISPLAY_R + 15, text="Солнце",
                       fill="#ffcc00", font=("Arial", 10, "bold"))

    # Орбиты
    for p in PLANETS:
        draw_orbit(p["distance"], zoom)

    # Планеты
    for p in PLANETS:
        # Угол = 2π * время / период (в годах)
        angle = 2 * math.pi * time_years / p["period"]

        # Позиция
        orbit_r = p["distance"] * zoom
        x = CX + orbit_r * math.cos(angle)
        y = CY + orbit_r * math.sin(angle)

        # Радиус планеты (для отображения)
        # Уменьшаем пропорционально, но чтобы видно было
        r = max(2, p["radius"] * 3)

        draw_planet(x, y, r, p["color"], p["name"])


def update():
    """Обновление каждый кадр (60 FPS)."""
    if state["running"]:
        # 1 секунда реального времени = скорость * дней
        # Для орбиты Нептуна (164.8 лет = 60166 дней)
        # нужно, чтобы за ~60 секунд был полный оборот
        # Значит: 60 сек = 60166 дней → 1 сек = 1000 дней
        # При speed=1 пройдёт 1000 дней ≈ 2.7 лет за 1 сек

        # Базовый шаг: 0.0001 "лет" за кадр, умноженный на speed
        base_step = 0.00005
        state["time"] += base_step * state["speed"]

    draw()
    root.after(16, update)  # ~60 FPS


# ==================== UI ПОЛЗУНКИ ====================
frame = tk.Frame(root, bg="#000010")
frame.pack(fill="x", padx=10, pady=5)

# ---- Ускорение времени ----
tk.Label(frame, text="Скорость времени:", fg="white", bg="#000010",
         font=("Arial", 11)).pack(side="left", padx=(10, 5))

speed_var = tk.DoubleVar(value=1.0)


def on_speed(value):
    state["speed"] = float(value)


speed_scale = ttk.Scale(frame, from_=1, to=100, orient="horizontal",
                        length=200, variable=speed_var,
                        command=on_speed)
speed_scale.pack(side="left")

speed_label = tk.Label(frame, text="×1", fg="#00ff00", bg="#000010",
                       font=("Arial", 11, "bold"))
speed_label.pack(side="left", padx=5)


def update_speed_label(*args):
    speed_label.config(text=f"×{int(speed_var.get())}")


speed_var.trace("w", update_speed_label)

# ---- Зум ----
tk.Label(frame, text="  Зум:", fg="white", bg="#000010",
         font=("Arial", 11)).pack(side="left", padx=(20, 5))

zoom_var = tk.DoubleVar(value=6.0)


def on_zoom(value):
    state["zoom"] = float(value)


zoom_scale = ttk.Scale(frame, from_=1, to=20, orient="horizontal",
                       length=200, variable=zoom_var,
                       command=on_zoom)
zoom_scale.pack(side="left")

zoom_label = tk.Label(frame, text="6x", fg="#00ff00", bg="#000010",
                      font=("Arial", 11, "bold"))
zoom_label.pack(side="left", padx=5)


def update_zoom_label(*args):
    zoom_label.config(text=f"{zoom_var.get():.1f}x")


zoom_var.trace("w", update_zoom_label)

# ---- Пауза / Продолжить ----
def toggle_pause():
    state["running"] = not state["running"]
    pause_btn.config(text="▶ Продолжить" if not state["running"] else "⏸ Пауза")


pause_btn = tk.Button(frame, text="⏸ Пауза", command=toggle_pause,
                      bg="#222244", fg="white", font=("Arial", 11),
                      relief="flat", padx=15, pady=5)
pause_btn.pack(side="left", padx=20)

# ---- Сброс ----
def reset_time():
    state["time"] = 0.0


reset_btn = tk.Button(frame, text="⟲ Сброс", command=reset_time,
                      bg="#222244", fg="white", font=("Arial", 11),
                      relief="flat", padx=15, pady=5)
reset_btn.pack(side="left")

# ==================== ИНФО-СТРОКА ====================
info = tk.Label(root, text="", fg="#888888", bg="#000010",
                font=("Arial", 9))
info.pack(side="bottom", pady=5)


def update_info():
    years = state["time"]
    days = years * 365.25
    info.config(text=f"Прошло: {years:.2f} лет  ({days:.0f} дней)")
    root.after(500, update_info)


# ==================== ЗАПУСК ====================
update_info()
update()
root.mainloop()
