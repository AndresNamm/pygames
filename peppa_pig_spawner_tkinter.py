import tkinter as tk
from tkinter import PhotoImage
import random
import time
import math

class PeppaPigSpawner:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Peppa Pig Spawner - Hold UP to spawn more!")
        
        # Make fullscreen
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='lightblue')
        
        # Get screen dimensions
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        # Create fullscreen canvas
        self.canvas = tk.Canvas(self.root, width=self.screen_width, height=self.screen_height, bg='lightblue')
        self.canvas.pack()
        
        # Add escape key to exit fullscreen
        self.root.bind('<Escape>', self.exit_fullscreen)
        
        # Try to load Peppa Pig image (tkinter supports GIF, PPM/PGM, some PNG)
        self.peppa_image = None
        try:
            # First try to load if it's a supported format
            self.peppa_image = PhotoImage(file="peppa.webp")
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
        self.animals = []  # Changed from peppa_pigs to animals
        self.up_pressed = False
        self.up_press_time = 0
        self.last_time = time.time()
        
        # Line spawning variables
        self.current_x = 100  # Starting x position
        self.current_y = 200  # Starting y position
        self.line_direction = 1  # 1 for right, -1 for left
        self.animal_spacing = 60  # Space between animals
        self.line_height_increment = 80  # How much to move down for new line
        
        # Bind keyboard events
        self.root.bind('<KeyPress-Up>', self.on_up_press)
        self.root.bind('<KeyRelease-Up>', self.on_up_release)
        self.root.bind('<KeyPress-Down>', self.on_down_press)
        self.root.bind('<KeyPress>', self.on_key_press)  # For focus
        self.root.focus_set()  # Make sure window can receive key events
        
        # Instructions
        center_x = self.screen_width // 2
        self.canvas.create_text(center_x, 30, text="Hold UP arrow to spawn Animals!", 
                               font=("Arial", 16, "bold"), fill="white")
        self.canvas.create_text(center_x, 55, text="Press DOWN to reset screen! Press ESC to exit fullscreen!", 
                               font=("Arial", 12), fill="white")
        
        # Start game loop
        self.game_loop()
    
    def exit_fullscreen(self, event):
        """Exit fullscreen mode when Escape is pressed"""
        self.root.attributes('-fullscreen', False)
        self.root.geometry("800x600")
    
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
        # Just reset the timer, don't clear pigs anymore
    
    def on_down_press(self, event):
        """Reset the screen when DOWN is pressed"""
        self.repaint_screen()
    
    def create_animal(self):
        # Use current line position instead of random
        x = self.current_x
        y = self.current_y
        size = random.randint(15, 80)  # Much wider size range: tiny to large
        
        # Different animals with their characteristic colors
        animals = [
            {'type': 'pig', 'colors': ['hotpink', 'pink', 'lightpink', 'deeppink'], 'symbol': '🐷'},
            {'type': 'sheep', 'colors': ['white', 'lightgray', 'ivory', 'snow'], 'symbol': '🐑'},
            {'type': 'lion', 'colors': ['gold', 'orange', 'goldenrod', 'darkorange'], 'symbol': '🦁'},
            {'type': 'cow', 'colors': ['black', 'white', 'gray', 'darkgray'], 'symbol': '🐄'},
            {'type': 'elephant', 'colors': ['gray', 'lightgray', 'darkgray', 'silver'], 'symbol': '🐘'},
            {'type': 'tiger', 'colors': ['orange', 'darkorange', 'coral', 'orangered'], 'symbol': '🐅'},
            {'type': 'horse', 'colors': ['brown', 'tan', 'chocolate', 'peru'], 'symbol': '🐴'},
            {'type': 'zebra', 'colors': ['black', 'white', 'darkslategray'], 'symbol': '🦓'},
            {'type': 'giraffe', 'colors': ['yellow', 'gold', 'khaki', 'palegoldenrod'], 'symbol': '🦒'},
            {'type': 'bear', 'colors': ['brown', 'saddlebrown', 'chocolate', 'sienna'], 'symbol': '🐻'}
        ]
        
        # Randomly select an animal type
        animal = random.choice(animals)
        color = random.choice(animal['colors'])
        
        # Update position for next animal
        self.current_x += self.animal_spacing * self.line_direction
        
        # Check if we need to start a new line
        if self.current_x > self.screen_width - 100 and self.line_direction == 1:
            # Hit right edge, start new line going left
            self.current_y += self.line_height_increment
            self.current_x = self.screen_width - 100
            self.line_direction = -1
        elif self.current_x < 100 and self.line_direction == -1:
            # Hit left edge, start new line going right
            self.current_y += self.line_height_increment
            self.current_x = 100
            self.line_direction = 1
        
        # Wrap around to top if we go too far down
        if self.current_y > self.screen_height - 100:
            self.current_y = 200
            self.current_x = 100
            self.line_direction = 1
        
        peppa = {
            'x': x,
            'y': y,
            'speed_x': 0,  # No movement - set to 0
            'speed_y': 0,  # No movement - set to 0
            'size': size,
            'color': color,
            'animal_type': animal['type'],
            'symbol': animal['symbol'],
            'id': None,
            'angle': random.uniform(0, 360),
            'rotation_speed': 0,  # No rotation - set to 0
            'bounce_factor': random.uniform(0.8, 1.2)
        }
        
        # Create visual representation
        if self.peppa_image:
            peppa['id'] = self.canvas.create_image(x, y, image=self.peppa_image)
            peppa['eyes'] = []  # No separate eyes for image
        else:
            # Create different shapes based on animal type
            if animal['type'] in ['sheep', 'bear']:
                # Round/fluffy animals - use circle
                peppa['id'] = self.canvas.create_oval(
                    x - size//2, y - size//2, x + size//2, y + size//2,
                    fill=color, outline='darkred', width=2
                )
            elif animal['type'] in ['horse', 'giraffe', 'zebra']:
                # Tall animals - use rectangle
                peppa['id'] = self.canvas.create_rectangle(
                    x - size//3, y - size//2, x + size//3, y + size//2,
                    fill=color, outline='black', width=2
                )
            elif animal['type'] in ['lion', 'tiger']:
                # Big cats - use diamond/polygon
                points = [x, y-size//2, x+size//2, y, x, y+size//2, x-size//2, y]
                peppa['id'] = self.canvas.create_polygon(
                    points, fill=color, outline='brown', width=2
                )
            else:
                # Default animals (pig, cow, elephant) - use oval
                peppa['id'] = self.canvas.create_oval(
                    x - size//2, y - size//2, x + size//2, y + size//2,
                    fill=color, outline='darkred', width=2
                )
            
            # Add eyes for all animals
            eye_size = max(2, size // 8)
            left_eye = self.canvas.create_oval(
                x - size//4, y - size//3, x - size//4 + eye_size, y - size//3 + eye_size,
                fill='black', outline=''
            )
            right_eye = self.canvas.create_oval(
                x + size//6, y - size//3, x + size//6 + eye_size, y - size//3 + eye_size,
                fill='black', outline=''
            )
            peppa['eyes'] = [left_eye, right_eye]
        
        # Add the animal to our list
        self.animals.append(peppa)
        
    def remove_animal(self):
        """Remove a random animal from the screen"""
        if self.animals:
            # Remove a random animal
            animal_to_remove = random.choice(self.animals)
            
            # Remove the visual element from canvas
            if animal_to_remove['id']:
                self.canvas.delete(animal_to_remove['id'])
                
            # Remove associated eyes if they exist
            if 'eyes' in animal_to_remove:
                for eye_id in animal_to_remove['eyes']:
                    self.canvas.delete(eye_id)
            
            # Remove from the list
            self.animals.remove(animal_to_remove)
    
    def clear_all_animals(self):
        """Remove all animals from the screen"""
        for animal in self.animals[:]:  # Copy list to avoid modification during iteration
            # Remove the visual element from canvas
            if animal['id']:
                self.canvas.delete(animal['id'])
                
            # Remove associated eyes if they exist
            if 'eyes' in animal:
                for eye_id in animal['eyes']:
                    self.canvas.delete(eye_id)
        
        # Clear the entire list
        self.animals.clear()
        print(f"Cleared all animals! Count now: {len(self.animals)}")  # Debug output
    
    def repaint_screen(self):
        """Clear the screen and repaint it fresh"""
        # Clear all animals first
        self.clear_all_animals()
        
        # Reset line position variables
        self.current_x = 100
        self.current_y = 200
        self.line_direction = 1
        
        # Clear the entire canvas
        self.canvas.delete("all")
        
        # Repaint the background color
        self.canvas.configure(bg='lightblue')
        
        # Redraw the instructions
        center_x = self.screen_width // 2
        self.canvas.create_text(center_x, 30, text="Hold UP arrow to spawn Animals!", 
                               font=("Arial", 16, "bold"), fill="white")
        self.canvas.create_text(center_x, 55, text="Press DOWN to reset screen! Press ESC to exit fullscreen!", 
                               font=("Arial", 12), fill="white")
        
        print("Screen repainted!")  # Debug output
    
    def update_animals(self, dt):
        for i, animal in enumerate(self.animals[:]):  # Copy list to avoid modification during iteration
            # Update position
            animal['x'] += animal['speed_x'] * dt
            animal['y'] += animal['speed_y'] * dt
            
            # Update rotation
            animal['angle'] += animal['rotation_speed'] * dt
            
            # Bounce off walls with some variation
            if animal['x'] <= animal['size']//2 or animal['x'] >= self.screen_width - animal['size']//2:
                animal['speed_x'] *= -animal['bounce_factor']
            if animal['y'] <= 100 or animal['y'] >= self.screen_height - animal['size']//2:
                animal['speed_y'] *= -animal['bounce_factor']
            
            # Keep within bounds
            animal['x'] = max(animal['size']//2, min(self.screen_width - animal['size']//2, animal['x']))
            animal['y'] = max(100, min(self.screen_height - animal['size']//2, animal['y']))
            
            # Update visual position
            if self.peppa_image:
                self.canvas.coords(animal['id'], animal['x'], animal['y'])
            else:
                # Update main body
                self.canvas.coords(animal['id'], 
                                 animal['x'] - animal['size']//2, animal['y'] - animal['size']//2,
                                 animal['x'] + animal['size']//2, animal['y'] + animal['size']//2)
                # Update eyes if they exist
                if 'eyes' in animal and len(animal['eyes']) >= 2:
                    eye_size = animal['size'] // 8
                    # Left eye
                    self.canvas.coords(animal['eyes'][0],
                                     animal['x'] - animal['size']//4, animal['y'] - animal['size']//3,
                                     animal['x'] - animal['size']//4 + eye_size, animal['y'] - animal['size']//3 + eye_size)
                    # Right eye  
                    self.canvas.coords(animal['eyes'][1],
                                     animal['x'] + animal['size']//6, animal['y'] - animal['size']//3,
                                     animal['x'] + animal['size']//6 + eye_size, animal['y'] - animal['size']//3 + eye_size)
    
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
                self.create_animal()
        
        # Update all Animals
        self.update_animals(dt)
        
        # Update stats display
        self.canvas.delete("stats")
        center_x = self.screen_width // 2
        spawn_rate = 15 if self.up_pressed else 0
        stats_text = f"Animals: {len(self.animals)}"
        if self.up_pressed:
            stats_text += f" | UP Hold Time: {self.up_press_time:.1f}s | Spawn Rate: {spawn_rate:.1f}/s"
        self.canvas.create_text(center_x, 80, text=stats_text, font=("Arial", 14), 
                               fill="white", tags="stats")
        
        # Add some visual feedback when keys are pressed
        center_x = self.screen_width // 2
        bottom_y = self.screen_height - 50
        if self.up_pressed:
            self.canvas.create_text(center_x, bottom_y, text="SPAWNING ANIMALS! Press DOWN to reset screen!", 
                                   font=("Arial", 16, "bold"), fill="yellow", tags="stats")
        elif self.animals:
            self.canvas.create_text(center_x, bottom_y, text="Hold UP to spawn more animals! Press DOWN to reset!", 
                                   font=("Arial", 14), fill="lightgreen", tags="stats")
        else:
            self.canvas.create_text(center_x, bottom_y, text="Hold UP to spawn animals! Press DOWN to reset!", 
                                   font=("Arial", 14), fill="lightblue", tags="stats")
        
        # Schedule next frame
        self.root.after(16, self.game_loop)  # ~60 FPS
    
    def run(self):
        print("FULLSCREEN ANIMAL SPAWNER!")
        print("Hold UP arrow key to spawn different animals!")
        print("Animals: Pigs🐷, Sheep🐑, Lions🦁, Cows🐄, Elephants🐘, Tigers🐅, Horses🐴, Zebras🦓, Giraffes🦒, Bears🐻")
        print("Press DOWN arrow key to reset the screen!")
        print("Press ESC to exit fullscreen, or close window to exit.")
        self.root.mainloop()

# Create and run the game
if __name__ == "__main__":
    game = PeppaPigSpawner()
    game.run()
