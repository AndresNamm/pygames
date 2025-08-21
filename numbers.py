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
                
        # Hide/show instructions in fullscreen
        if self.fullscreen:
            self.instructions.pack_forget()
        else:
            self.instructions.pack(side="bottom", pady=10)
    
    def exit_fullscreen_or_quit(self):
        """Exit fullscreen if in fullscreen mode, otherwise quit the game"""
        if self.fullscreen:
            self.fullscreen = False
            try:
                self.root.attributes("-fullscreen", False)
            except Exception:
                self.root.state('normal')
            self.instructions.pack(side="bottom", pady=10)
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
