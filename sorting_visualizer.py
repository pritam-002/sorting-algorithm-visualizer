import tkinter as tk
import random
import time

# Global variables
barList = []
lengthList = []
worker = None
start_time = 0
bar_count = 0

# Swap animation
def swap(pos_0, pos_1):
    bar11, _, bar12, _ = canvas.coords(pos_0)
    bar21, _, bar22, _ = canvas.coords(pos_1)
    canvas.move(pos_0, bar21 - bar11, 0)
    canvas.move(pos_1, bar12 - bar22, 0)

# Sorting Algorithms
def _bubble_sort():
    global barList, lengthList
    for i in range(len(lengthList) - 1):
        for j in range(len(lengthList) - i - 1):
            if lengthList[j] > lengthList[j + 1]:
                lengthList[j], lengthList[j + 1] = lengthList[j + 1], lengthList[j]
                barList[j], barList[j + 1] = barList[j + 1], barList[j]
                swap(barList[j + 1], barList[j])
                yield

def _selection_sort():
    global barList, lengthList
    for i in range(len(lengthList)):
        min_idx = i
        for j in range(i + 1, len(lengthList)):
            if lengthList[j] < lengthList[min_idx]:
                min_idx = j
        if min_idx != i:
            lengthList[min_idx], lengthList[i] = lengthList[i], lengthList[min_idx]
            barList[min_idx], barList[i] = barList[i], barList[min_idx]
            swap(barList[min_idx], barList[i])
            yield

def _insertion_sort():
    global barList, lengthList
    for i in range(len(lengthList)):
        cursor = lengthList[i]
        cursorBar = barList[i]
        pos = i
        while pos > 0 and lengthList[pos - 1] > cursor:
            lengthList[pos] = lengthList[pos - 1]
            barList[pos], barList[pos - 1] = barList[pos - 1], barList[pos]
            swap(barList[pos], barList[pos - 1])
            yield
            pos -= 1
        lengthList[pos] = cursor
        barList[pos] = cursorBar

def _quick_sort(start, end):
    if start >= end:
        return
    pivot = lengthList[end]
    i = start
    for j in range(start, end):
        if lengthList[j] < pivot:
            lengthList[i], lengthList[j] = lengthList[j], lengthList[i]
            barList[i], barList[j] = barList[j], barList[i]
            swap(barList[i], barList[j])
            yield
            i += 1
    lengthList[i], lengthList[end] = lengthList[end], lengthList[i]
    barList[i], barList[end] = barList[end], barList[i]
    swap(barList[i], barList[end])
    yield
    yield from _quick_sort(start, i - 1)
    yield from _quick_sort(i + 1, end)

def _heapify(n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and lengthList[l] > lengthList[largest]:
        largest = l
    if r < n and lengthList[r] > lengthList[largest]:
        largest = r
    if largest != i:
        lengthList[i], lengthList[largest] = lengthList[largest], lengthList[i]
        barList[i], barList[largest] = barList[largest], barList[i]
        swap(barList[i], barList[largest])
        yield
        yield from _heapify(n, largest)

def _heap_sort():
    n = len(lengthList)
    for i in range(n // 2 - 1, -1, -1):
        yield from _heapify(n, i)
    for i in range(n - 1, 0, -1):
        lengthList[0], lengthList[i] = lengthList[i], lengthList[0]
        barList[0], barList[i] = barList[i], barList[0]
        swap(barList[0], barList[i])
        yield
        yield from _heapify(i, 0)

# Animate sorting
def animate():
    global worker
    try:
        next(worker)
        window.after(20, animate)
    except StopIteration:
        elapsed_time = round(time.time() - start_time, 4)
        time_label.config(text=f"Time Taken: {elapsed_time} seconds")
        worker = None

# Mapping for dropdown
sort_algorithms = {
    "Bubble Sort": (_bubble_sort, "O(n^2)"),
    "Selection Sort": (_selection_sort, "O(n^2)"),
    "Insertion Sort": (_insertion_sort, "O(n^2)"),
    "Quick Sort": (lambda: _quick_sort(0, len(lengthList) - 1), "O(n log n)"),
    "Heap Sort": (_heap_sort, "O(n log n)")
}

# Run sorting algorithm
def run_sort():
    global worker, start_time
    selected_algo = algo_var.get()
    if selected_algo in sort_algorithms:
        func, complexity = sort_algorithms[selected_algo]
        complexity_label.config(text=f"Time Complexity: {complexity}")
        start_time = time.time()
        worker = func()
        animate()

def generate():
    global barList, lengthList, bar_count
    try:
        bar_count = int(entry_bars.get())
        if bar_count <= 0 or bar_count > 100:
            raise ValueError
    except ValueError:
        error_label.config(text="Please enter a valid positive integer (1–100).")
        return

    error_label.config(text="")
    canvas.delete("all")
    barList.clear()
    lengthList.clear()

    canvas_width = 980
    canvas_height = 400

    # Choose a fixed bar width based on total count (auto scales)
    bar_width = max(5, min(20, (canvas_width - 10) // bar_count))
    total_bar_width = bar_width * bar_count
    total_spacing = canvas_width - total_bar_width
    spacing = total_spacing // (bar_count + 1)

    x = spacing
    for _ in range(bar_count):
        height = random.randint(20, 360)
        y0 = canvas_height - height
        x0 = x
        x1 = x0 + bar_width
        bar = canvas.create_rectangle(x0, y0, x1, canvas_height, fill="yellow")
        barList.append(bar)
        lengthList.append(height)
        x = x1 + spacing

    # Highlight min and max
    min_val = min(lengthList)
    max_val = max(lengthList)
    for i in range(bar_count):
        if lengthList[i] == min_val:
            canvas.itemconfig(barList[i], fill="red")
        elif lengthList[i] == max_val:
            canvas.itemconfig(barList[i], fill="green")

    time_label.config(text="Time Taken: N/A")
    complexity_label.config(text="Time Complexity: N/A")




# Reset all
def reset():
    global worker
    if worker:
        try:
            next(worker)
        except StopIteration:
            pass
    canvas.delete("all")
    barList.clear()
    lengthList.clear()
    entry_bars.delete(0, tk.END)
    time_label.config(text="Time Taken: N/A")
    complexity_label.config(text="Time Complexity: N/A")
    algo_var.set("Select Sorting Algorithm")
    error_label.config(text="")
    worker = None

#  GUI Setup 
window = tk.Tk()
window.title("Sorting Algorithm Visualizer")
window.geometry("1000x650")
window.configure(bg="black")

tk.Label(window, text="Sorting Algorithm Visualizer", font=("Helvetica", 16, "bold"), 
         bg="lightblue", fg="black").pack(fill=tk.X, pady=(0, 5))
tk.Label(window, text="Project by: Pritam Roy", font=("Courier", 10), 
         bg="black", fg="white").pack(pady=(0, 10))

# Control Frame
control_frame = tk.Frame(window, bg="black")
control_frame.pack(pady=10)

tk.Label(control_frame, text="Number of Bars (1-100):", bg='black', fg='white',
         font=("Helvetica", 10)).grid(row=0, column=0, padx=5)
entry_bars = tk.Entry(control_frame, width=10, font=("Helvetica", 10))
entry_bars.grid(row=0, column=1, padx=5)

tk.Button(control_frame, text="Generate", command=generate, bg="lightyellow",
          font=("Helvetica", 10), width=8).grid(row=0, column=2, padx=5)

algo_var = tk.StringVar()
algo_var.set("Select Sorting Algorithm")
algo_menu = tk.OptionMenu(control_frame, algo_var, *sort_algorithms.keys())
algo_menu.config(bg="lightgreen", font=("Helvetica", 10), width=20)
algo_menu.grid(row=0, column=3, padx=5)

tk.Button(control_frame, text="Sort", command=run_sort, bg="lightblue",
          font=("Helvetica", 10), width=8).grid(row=0, column=4, padx=5)
tk.Button(control_frame, text="Reset", command=reset, bg="red", fg="white",
          font=("Helvetica", 10), width=8).grid(row=0, column=5, padx=5)

# Labels
info_frame = tk.Frame(window, bg="black")
info_frame.pack(pady=5)

time_label = tk.Label(info_frame, text="Time Taken: N/A", bg="black", 
                      fg="white", font=("Helvetica", 10))
time_label.pack(side=tk.LEFT, padx=20)

complexity_label = tk.Label(info_frame, text="Time Complexity: N/A", bg="black", 
                           fg="white", font=("Helvetica", 10))
complexity_label.pack(side=tk.LEFT, padx=20)

error_label = tk.Label(window, text="", fg="red", bg="black", font=("Helvetica", 10))
error_label.pack()

# Canvas
canvas = tk.Canvas(window, width=980, height=400, bg="black", highlightthickness=1,
                  highlightbackground="white")
canvas.pack(pady=10)

# Initial instructions
instructions = tk.Label(window, text="1. Enter number of bars (1-100) 2. Click Generate 3. Select algorithm 4. Click Sort",
                       bg="black", fg="cyan", font=("Helvetica", 10))
instructions.pack()

window.mainloop()









