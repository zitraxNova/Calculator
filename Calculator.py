import tkinter as tk


# Функции калькулятора
def add_to_expression(value):
    current = display_var.get()
    display_var.set(current + value)


def calculate():
    try:
        result = str(eval(display_var.get()))
        display_var.set(result)
    except Exception:
        display_var.set("Ошибка")


def clear():
    display_var.set("")


def interpolate_color(c1, c2, t):
    r = int(c1[0] + (c2[0] - c1[0]) * t)
    g = int(c1[1] + (c2[1] - c1[1]) * t)
    b = int(c1[2] + (c2[2] - c1[2]) * t)
    return f"#{r:02x}{g:02x}{b:02x}"


def round_button(parent, x, y, text, cmd):
    canvas = tk.Canvas(
        parent, width=80, height=80,
        bg="black", highlightthickness=0)
    circle = canvas.create_oval(5, 5, 75, 75, fill="#ffffff", outline="#d0d0d0", width=2)
    label = canvas.create_text(40, 40, text=text, fill="black", font=("Arial", 20, "bold"))
    # цвета для анимации
    base_color = (255, 255, 255)
    hover_color = (235, 235, 235)
    anim_steps = 10
    anim_time = 15
    canvas.hovering = False
    canvas.anim_job = None

    def animate(to_hover):
        if canvas.anim_job:
            canvas.after_cancel(canvas.anim_job)

        def step(i):
            t = i / anim_steps
            if not to_hover:
                t = 1 - t
            new_color = interpolate_color(base_color, hover_color, t)
            canvas.itemconfig(circle, fill=new_color)
            if i < anim_steps:
                canvas.anim_job = canvas.after(anim_time, step, i + 1)
        step(0)

    def on_enter(event):
        canvas.hovering = True
        animate(True)

    def on_leave(event):
        canvas.hovering = False
        animate(False)

    def on_click(event):
        cmd()

    canvas.bind("<Button-1>", on_click)
    canvas.bind("<Enter>", on_enter)
    canvas.bind("<Leave>", on_leave)
    canvas.grid(row=y, column=x, padx=10, pady=10)
    return canvas

root = tk.Tk()
root.title("Calculator")
root.configure(bg="black")
display_var = tk.StringVar()
display = tk.Entry(
    root, textvariable=display_var, font=("Arial", 28),
    bg="black", fg="white", justify="right", bd=0, highlightthickness=0)
display.grid(row=0, column=0, columnspan=4, padx=10, pady=20, ipady=20)
# Расположение кнопок
buttons = [
    ("7", 0, 1), ("8", 1, 1), ("9", 2, 1), ("/", 3, 1),
    ("4", 0, 2), ("5", 1, 2), ("6", 2, 2), ("*", 3, 2),
    ("1", 0, 3), ("2", 1, 3), ("3", 2, 3), ("-", 3, 3),
    ("0", 0, 4), (".", 1, 4), ("=", 2, 4), ("+", 3, 4),
]
for text, x, y in buttons:
    if text == "=":
        round_button(root, x, y, text, calculate)
    else:
        round_button(root, x, y, text, lambda v=text: add_to_expression(v))
# Нижний ряд
round_button(root, 0, 5, "C", clear)
round_button(root, 1, 5, "(", lambda: add_to_expression("("))
round_button(root, 2, 5, ")", lambda: add_to_expression(")"))
root.mainloop()
