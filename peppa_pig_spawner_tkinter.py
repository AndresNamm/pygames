import tkinter as tk
from tkinter import PhotoImage
import random
import time
import math

class PeppaPigSpawner:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Peppa Pig Spawner - Hold UP to spawn more!")
        self.root.geometry("800x600")
        self.root.configure(bg='lightblue')
        
        # Create canvas
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg='lightblue')
        self.canvas.pack()
        
        # Try to load Peppa Pig image (tkinter supports GIF, PPM/PGM, some PNG)
        self.peppa_image = None
        try:
            # First try to load if it's a supported format
            self.peppa_image = PhotoImage(file="Peppa_Pig.webp")
            # Scale down the image if it's too large
            if self.peppa_image.width() > 60:
                scale_factor = max(1, self.peppa_image.width() // 60)
                self.peppa_image = self.peppa_image.subsample(scale_factor)
        except (tk.TclError, FileNotFoundError):
            # If image can't be loaded, we'll use simple shapes instead
            self.peppa_image = None
            print("Could not load Peppa_Pig.webp (tkinter has limited image format support).")
            print("Using colorful shapes instead of images!")
        
        # Game variables
        self.peppa_pigs = []
        self.up_pressed = False
        self.down_pressed = False
        self.up_press_time = 0
        self.down_press_time = 0
        self.last_time = time.time()
        
        # Bind keyboard events
        self.root.bind('<KeyPress-Up>', self.on_up_press)
        self.root.bind('<KeyRelease-Up>', self.on_up_release)
        self.root.bind('<KeyPress-Down>', self.on_down_press)
        self.root.bind('<KeyRelease-Down>', self.on_down_release)
        self.root.bind('<KeyPress>', self.on_key_press)  # For focus
        self.root.focus_set()  # Make sure window can receive key events
        
        # Instructions
        self.canvas.create_text(400, 30, text="Hold UP arrow to spawn Peppa Pigs!", 
                               font=("Arial", 16, "bold"), fill="white")
        self.canvas.create_text(400, 55, text="Release UP to repaint screen!", 
                               font=("Arial", 12), fill="white")
        
        # Start game loop
        self.game_loop()
    
    def on_key_press(self, event):
        # This helps maintain focus for key events
        pass
    
    def on_up_press(self, event):
        if not self.up_pressed:
            self.up_pressed = True
            self.up_press_time = 0
    
    def on_up_release(self, event):
        self.up_pressed = False
        self.up_press_time = 0
        # Repaint/clear the screen when UP is released
        self.repaint_screen()
    
    def on_down_press(self, event):
        if not self.down_pressed:
            self.down_pressed = True
            self.down_press_time = 0
    
    def on_down_release(self, event):
        self.down_pressed = False
        self.down_press_time = 0
        # Clear all pigs when DOWN is released
        self.clear_all_pigs()
    
    def create_peppa_pig(self):
        x = random.randint(50, 750)
        y = random.randint(100, 550)
        size = random.randint(25, 45)
        
        # Random colors for variety
        colors = ['hotpink', 'pink', 'lightpink', 'deeppink', 'magenta', 'orchid']
        color = random.choice(colors)
        
        peppa = {
            'x': x,
            'y': y,
            'speed_x': random.uniform(-80, 80),  # pixels per second
            'speed_y': random.uniform(-80, 80),
            'size': size,
            'color': color,
            'id': None,
            'angle': random.uniform(0, 360),
            'rotation_speed': random.uniform(-180, 180),  # degrees per second
            'bounce_factor': random.uniform(0.8, 1.2)
        }
        
        # Create visual representation
        if self.peppa_image:
            peppa['id'] = self.canvas.create_image(x, y, image=self.peppa_image)
            peppa['eyes'] = []  # No separate eyes for image
        else:
            # Create a cute pig-like shape with multiple elements
            # Main body (oval)
            peppa['id'] = self.canvas.create_oval(
                x - size//2, y - size//2, x + size//2, y + size//2,
                fill=color, outline='darkred', width=2
            )
            # Add some "eyes" as small circles and store their IDs
            eye_size = size // 8
            left_eye = self.canvas.create_oval(
                x - size//4, y - size//3, x - size//4 + eye_size, y - size//3 + eye_size,
                fill='black', outline=''
            )
            right_eye = self.canvas.create_oval(
                x + size//6, y - size//3, x + size//6 + eye_size, y - size//3 + eye_size,
                fill='black', outline=''
            )
            peppa['eyes'] = [left_eye, right_eye]
        
    def remove_peppa_pig(self):
        """Remove a random Peppa Pig from the screen"""
        if self.peppa_pigs:
            # Remove a random pig
            pig_to_remove = random.choice(self.peppa_pigs)
            
            # Remove the visual element from canvas
            if pig_to_remove['id']:
                self.canvas.delete(pig_to_remove['id'])
                
            # Remove associated eyes if they exist
            if 'eyes' in pig_to_remove:
                for eye_id in pig_to_remove['eyes']:
                    self.canvas.delete(eye_id)
            
            # Remove from the list
            self.peppa_pigs.remove(pig_to_remove)
    
    def clear_all_pigs(self):
        """Remove all Peppa Pigs from the screen"""
        for pig in self.peppa_pigs[:]:  # Copy list to avoid modification during iteration
            # Remove the visual element from canvas
            if pig['id']:
                self.canvas.delete(pig['id'])
                
            # Remove associated eyes if they exist
            if 'eyes' in pig:
                for eye_id in pig['eyes']:
                    self.canvas.delete(eye_id)
        
        # Clear the entire list
        self.peppa_pigs.clear()
        print(f"Cleared all pigs! Count now: {len(self.peppa_pigs)}")  # Debug output
    
    def repaint_screen(self):
        """Clear the screen and repaint it fresh"""
        # Clear all pigs first
        self.clear_all_pigs()
        
        # Clear the entire canvas
        self.canvas.delete("all")
        
        # Repaint the background color
        self.canvas.configure(bg='lightblue')
        
        # Redraw the instructions
        self.canvas.create_text(400, 30, text="Hold UP arrow to spawn Peppa Pigs!", 
                               font=("Arial", 16, "bold"), fill="white")
        self.canvas.create_text(400, 55, text="Release DOWN arrow to clear all pigs!", 
                               font=("Arial", 12), fill="white")
        
        print("Screen repainted!")  # Debug output
    
    def update_peppa_pigs(self, dt):
        for i, peppa in enumerate(self.peppa_pigs[:]):  # Copy list to avoid modification during iteration
            # Update position
            peppa['x'] += peppa['speed_x'] * dt
            peppa['y'] += peppa['speed_y'] * dt
            
            # Update rotation
            peppa['angle'] += peppa['rotation_speed'] * dt
            
            # Bounce off walls with some variation
            if peppa['x'] <= peppa['size']//2 or peppa['x'] >= 800 - peppa['size']//2:
                peppa['speed_x'] *= -peppa['bounce_factor']
            if peppa['y'] <= 100 or peppa['y'] >= 600 - peppa['size']//2:
                peppa['speed_y'] *= -peppa['bounce_factor']
            
            # Keep within bounds
            peppa['x'] = max(peppa['size']//2, min(800 - peppa['size']//2, peppa['x']))
            peppa['y'] = max(100, min(600 - peppa['size']//2, peppa['y']))
            
            # Update visual position
            if self.peppa_image:
                self.canvas.coords(peppa['id'], peppa['x'], peppa['y'])
            else:
                # Update main body
                self.canvas.coords(peppa['id'], 
                                 peppa['x'] - peppa['size']//2, peppa['y'] - peppa['size']//2,
                                 peppa['x'] + peppa['size']//2, peppa['y'] + peppa['size']//2)
                # Update eyes if they exist
                if 'eyes' in peppa and len(peppa['eyes']) >= 2:
                    eye_size = peppa['size'] // 8
                    # Left eye
                    self.canvas.coords(peppa['eyes'][0],
                                     peppa['x'] - peppa['size']//4, peppa['y'] - peppa['size']//3,
                                     peppa['x'] - peppa['size']//4 + eye_size, peppa['y'] - peppa['size']//3 + eye_size)
                    # Right eye  
                    self.canvas.coords(peppa['eyes'][1],
                                     peppa['x'] + peppa['size']//6, peppa['y'] - peppa['size']//3,
                                     peppa['x'] + peppa['size']//6 + eye_size, peppa['y'] - peppa['size']//3 + eye_size)
    
    def game_loop(self):
        current_time = time.time()
        dt = current_time - self.last_time
        self.last_time = current_time
        
        # Handle UP key being held down
        if self.up_pressed:
            self.up_press_time += dt
            # Spawn rate increases with time held (exponential growth) - MUCH FASTER!
            spawn_rate = 15  # Increased from 5 to 15 spawns per second
            
            # Spawn Peppa Pigs based on spawn rate
            if random.random() < spawn_rate * dt:
                self.create_peppa_pig()
        
        # Handle DOWN key being held down
        if self.down_pressed:
            self.down_press_time += dt
            # Remove pigs when DOWN is held - faster the longer you hold
            despawn_rate = max(5, min(self.down_press_time * 5, 20))  # Start at 5, cap at 20 removals per second
            
            if self.peppa_pigs and random.random() < despawn_rate * dt:
                print(f"Removing pig with DOWN! Current count: {len(self.peppa_pigs)}")  # Debug output
                self.remove_peppa_pig()
        
        # Update all Peppa Pigs
        self.update_peppa_pigs(dt)
        
        # Update stats display
        self.canvas.delete("stats")
        spawn_rate = 15 if self.up_pressed else 0  # Updated to match new faster rate
        despawn_rate_display = max(5, min(self.down_press_time * 5, 20)) if self.down_pressed else 0
        stats_text = f"Peppa Pigs: {len(self.peppa_pigs)}"
        if self.up_pressed:
            stats_text += f" | UP Hold Time: {self.up_press_time:.1f}s | Spawn Rate: {spawn_rate:.1f}/s"
        if self.down_pressed:
            stats_text += f" | DOWN Hold Time: {self.down_press_time:.1f}s | Despawn Rate: {despawn_rate_display:.1f}/s"
        self.canvas.create_text(400, 80, text=stats_text, font=("Arial", 10), 
                               fill="white", tags="stats")
        
        # Add some visual feedback when keys are pressed
        if self.up_pressed:
            self.canvas.create_text(400, 550, text="SPAWNING PEPPA PIGS! Release to repaint!", 
                                   font=("Arial", 14, "bold"), fill="yellow", tags="stats")
        elif self.down_pressed:
            self.canvas.create_text(400, 550, text="HOLD DOWN - RELEASE TO CLEAR ALL!", 
                                   font=("Arial", 14, "bold"), fill="red", tags="stats")
        elif self.peppa_pigs:
            self.canvas.create_text(400, 550, text="Release UP to repaint, DOWN to clear!", 
                                   font=("Arial", 12), fill="lightgreen", tags="stats")
        
        # Schedule next frame
        self.root.after(16, self.game_loop)  # ~60 FPS
    
    def run(self):
        print("Use UP arrow key to spawn Peppa Pigs!")
        print("Release UP to repaint the entire screen!")
        print("Press and release DOWN arrow key to clear all pigs!")
        print("Close the window to exit.")
        self.root.mainloop()

# Create and run the game
if __name__ == "__main__":
    game = PeppaPigSpawner()
    game.run()
