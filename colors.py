import tkinter as tk

# List of colors to cycle through
COLORS = ["green", "red", "blue", "yellow", "pink", "orange", "purple","black", "white"]

class ColorCycleGame:
    def __init__(self, root):
        self.root = root
        self.index = 0
        self.fullscreen = False  # track fullscreen state
        self.root.title("Color Cycle Game")
        self.root.geometry("600x400")
        self.root.configure(bg=COLORS[self.index])
        # Removed text label; now the window just shows the color.

        # Key bindings
        root.bind("<space>", self.next_color)
        root.bind("<Right>", self.next_color)
        root.bind("<Return>", self.next_color)
        root.bind("<Left>", self.prev_color)
        root.bind("q", self.quit)
        root.bind("Q", self.quit)
        root.bind("<Escape>", self.exit_fullscreen_or_quit)
        root.bind("f", self.toggle_fullscreen)
        root.bind("F", self.toggle_fullscreen)

    # Removed _label_text method

    def _apply_color(self):
        color = COLORS[self.index]
        self.root.configure(bg=color)

    def next_color(self, event=None):
        self.index = (self.index + 1) % len(COLORS)
        self._apply_color()

    def prev_color(self, event=None):
        self.index = (self.index - 1) % len(COLORS)
        self._apply_color()

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        try:
            self.root.attributes("-fullscreen", self.fullscreen)
        except Exception:
            # Fallback: zoomed state for platforms where fullscreen attr unsupported
            if self.fullscreen:
                self.root.state('zoomed')
            else:
                self.root.state('normal')

    def exit_fullscreen_or_quit(self, event=None):
        if self.fullscreen:
            self.fullscreen = False
            try:
                self.root.attributes("-fullscreen", False)
            except Exception:
                self.root.state('normal')
        else:
            self.quit()

    def quit(self, event=None):
        self.root.destroy()


def main():
    root = tk.Tk()
    ColorCycleGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
