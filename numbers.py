import tkinter as tk
from tkinter import font

class NumberCycleGame:
    def __init__(self, root):
        self.root = root
        self.numbers = [str(n) for n in range(1, 10)]
        self.current_index = 0
        self.fullscreen = False
        
        # Configure the window
        self.root.title("Number Cycle Game")
        self.root.geometry("800x600")
        self.root.configure(bg="black")
        
        # Create a large font for the numbers
        self.large_font = font.Font(family="Arial", size=200, weight="bold")
        
        # Create the label to display the number
        self.number_label = tk.Label(
            self.root,
            text=self.numbers[self.current_index],
            font=self.large_font,
            fg="white",
            bg="black"
        )
        self.number_label.pack(expand=True)
        
        # Create canvas for drawing bars
        self.canvas = tk.Canvas(
            self.root,
            height=100,
            bg="black",
            highlightthickness=0
        )
        self.canvas.pack(fill="x", padx=20, pady=10)
        
        # Draw initial bars
        self.draw_bars()
        
        # Instructions label
        self.instructions = tk.Label(
            self.root,
            text="Press any key to cycle through numbers (1-9) | F = Toggle Fullscreen | ESC/Q = Quit",
            font=("Arial", 12),
            fg="gray",
            bg="black"
        )
        self.instructions.pack(side="bottom", pady=10)
        
        # Bind key events
        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.focus_set()  # Ensure the window can receive key events
        
    def cycle_number(self):
        """Move to the next number in the sequence"""
        self.current_index = (self.current_index + 1) % len(self.numbers)
        self.number_label.config(text=self.numbers[self.current_index])
        self.draw_bars()  # Update bars when number changes
        
    def draw_bars(self):
        """Draw bars equal to the current number"""
        self.canvas.delete("all")  # Clear previous bars
        
        current_number = int(self.numbers[self.current_index])
        canvas_width = self.canvas.winfo_width()
        
        # If canvas width is not available yet, use a default or schedule for later
        if canvas_width <= 1:
            self.root.after(50, self.draw_bars)
            return
            
        bar_width = 40
        bar_height = 60
        spacing = 10
        total_width = (bar_width * current_number) + (spacing * (current_number - 1))
        start_x = (canvas_width - total_width) // 2
        
        for i in range(current_number):
            x1 = start_x + (i * (bar_width + spacing))
            x2 = x1 + bar_width
            y1 = 20
            y2 = y1 + bar_height
            
            # Create a colored bar
            self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill="lightblue",
                outline="white",
                width=2
            )
        
    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        self.fullscreen = not self.fullscreen
        try:
            self.root.attributes("-fullscreen", self.fullscreen)
        except Exception:
            # Fallback for platforms where fullscreen attribute is not supported
            if self.fullscreen:
                self.root.state('zoomed')
            else:
                self.root.state('normal')
                
        # Hide/show instructions and canvas in fullscreen
        if self.fullscreen:
            self.instructions.pack_forget()
            self.canvas.pack_forget()
        else:
            self.instructions.pack(side="bottom", pady=10)
            self.canvas.pack(fill="x", padx=20, pady=10)
            # Redraw bars after showing canvas
            self.root.after(50, self.draw_bars)
    
    def exit_fullscreen_or_quit(self):
        """Exit fullscreen if in fullscreen mode, otherwise quit the game"""
        if self.fullscreen:
            self.fullscreen = False
            try:
                self.root.attributes("-fullscreen", False)
            except Exception:
                self.root.state('normal')
            self.instructions.pack(side="bottom", pady=10)
            self.canvas.pack(fill="x", padx=20, pady=10)
            # Redraw bars after showing canvas
            self.root.after(50, self.draw_bars)
        else:
            self.quit_game()
    
    def quit_game(self):
        """Close the game"""
        self.root.destroy()
    
    def on_key_press(self, event):
        """Handle key press events"""
        key = event.keysym.lower()
        
        if key == 'f':
            self.toggle_fullscreen()
        elif key in ['escape', 'q']:
            self.exit_fullscreen_or_quit()
        else:
            # Any other key cycles through the numbers
            self.cycle_number()

def main():
    root = tk.Tk()
    game = NumberCycleGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
