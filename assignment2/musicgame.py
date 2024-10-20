import pygame
import random
import time
import librosa


pygame.init()


# Set screen dimensions and colors
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FONT = pygame.font.Font(None, 36)
NOTE_RADIUS = 50  
NOTE_LIFETIME = 2  
GREAT_THRESHOLD = 0.1
GOOD_THRESHOLD = 0.3
score = 0


# Set up screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Music game")
icon = pygame.image.load('assignment2/assets/icon.png')
pygame.display.set_icon(icon)


# Note class
class Note:
    def __init__(self, x, y, appear_time):
        self.x = x
        self.y = y
        self.appear_time = appear_time
        self.hit_time = None
        self.image = pygame.image.load('assignment2/assets/note.png')  


    def draw(self):
        current_time = time.time()
        if current_time - self.appear_time < NOTE_LIFETIME:
            alpha = int(255 * (1 - (current_time - self.appear_time) / NOTE_LIFETIME))
            self.image.set_alpha(alpha)  # Set image transparency
            screen.blit(self.image, (self.x - self.image.get_width() // 2, self.y - self.image.get_height() // 2))
    
    def is_clicked(self, click_time, pos):
        current_time = time.time()
        alpha = int(255 * (1 - (current_time - self.appear_time) / NOTE_LIFETIME))
        if self.hit_time is None and alpha > 127:  # Check if note is clickable
            distance = ((pos[0] - self.x) ** 2 + (pos[1] - self.y) ** 2) ** 0.5
            if distance <= NOTE_RADIUS:
                self.hit_time = click_time - self.appear_time
                return True
        return False


    def get_feedback(self):
        if self.hit_time is not None:
            return "Great"
        return None


# Generate notes from audio
def generate_notes_from_audio(audio_path):
    y, sr = librosa.load(audio_path)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr, start=0.5)
    notes = []
    for beat in beats:
        x = random.randint(NOTE_RADIUS, SCREEN_WIDTH - NOTE_RADIUS)
        y = random.randint(NOTE_RADIUS, SCREEN_HEIGHT - NOTE_RADIUS)
        appear_time = beat / sr + time.time()
        notes.append(Note(x, y, appear_time))
    return notes


def show_pause_menu():
    screen.fill(BLACK)
    pause_text = FONT.render("Game Paused", True, WHITE)
    screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 2 - pause_text.get_height() // 2 - 50))


    # Create buttons
    restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50)
    continue_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 120, 200, 50)
    quit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 190, 200, 50)
    restart_image = pygame.image.load('assignment2/assets/btn_re.jpg')
    continue_image = pygame.image.load('assignment2/assets/btn_con.jpg')
    quit_image = pygame.image.load('assignment2/assets/btn_quit.jpg')
    screen.blit(restart_image, (restart_button.x, restart_button.y))
    screen.blit(continue_image, (continue_button.x, continue_button.y))
    screen.blit(quit_image, (quit_button.x, quit_button.y))


    pygame.display.flip()


    # Wait for user input
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if restart_button.collidepoint(pos):
                    return True
                elif continue_button.collidepoint(pos):
                    return "continue"
                elif quit_button.collidepoint(pos):
                    return False
    return False



def show_summary():
    global score
    screen.fill(BLACK)
    summary_text = FONT.render(f"Final Score: {score}", True, WHITE)
    screen.blit(summary_text, (SCREEN_WIDTH // 2 - summary_text.get_width() // 2, SCREEN_HEIGHT // 2 - summary_text.get_height() // 2))


    # Create buttons
    restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50)
    quit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 120, 200, 50)
    restart_image = pygame.image.load('assignment2/assets/btn_re.jpg')
    quit_image = pygame.image.load('assignment2/assets/btn_quit.jpg')
    screen.blit(restart_image, (restart_button.x, restart_button.y))
    screen.blit(quit_image, (quit_button.x, quit_button.y))


    pygame.display.flip()


    # Wait for user input
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if restart_button.collidepoint(pos):
                    return True
                elif quit_button.collidepoint(pos):
                    waiting = False
                    return False
    return False


def show_start_menu():
    screen.fill(BLACK)
    background_image = pygame.image.load('assignment2/assets/bg1.png')
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  
    screen.blit(background_image, (0, 0))


    start_image = pygame.image.load('assignment2/assets/btn_start.jpg') 
    start_rect = start_image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100))
    screen.blit(start_image, start_rect)


    pygame.display.flip()


    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return show_instructions()



    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return show_instructions()


# Game instructions
def show_instructions():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 32)
    text = font.render("Game Instructions: ", True, WHITE)
    screen.blit(text, (10, 10))


    text = font.render("Click the notes on the screen according to the rhythm!", True, WHITE)
    screen.blit(text, (10, 50))


    text = font.render("Your score is displayed at the end of the game", True, WHITE)
    screen.blit(text, (10, 90))


    ok_button = pygame.Rect(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100, 100, 50)
    ok_image = pygame.image.load('assignment2/assets/btn_ok.jpg')
    screen.blit(ok_image, (ok_button.x, ok_button.y))


    pygame.display.flip()


    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if ok_button.collidepoint(pos):
                    # Show loading screen
                    screen.fill(BLACK)
                    loading_text = FONT.render("Loading...", True, WHITE)
                    screen.blit(loading_text, (SCREEN_WIDTH // 2 - loading_text.get_width() // 2, SCREEN_HEIGHT // 2 - loading_text.get_height() // 2))
                    pygame.display.flip()
                    pygame.time.wait(1000)  
                    return True
                
# Main game loop
def main_game_loop():
    global score
    running = True
    clock = pygame.time.Clock()
    start_time = time.time()
    feedback_text = "" 
    feedback_time = 0  


    # Load audio and generate notes
    audio_path = 'assignment2/assets/sound1.mp3' 
    y, sr = librosa.load(audio_path)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beats, sr=sr)
    next_beat_index = 0
    notes = []


    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()


    click_sound = pygame.mixer.Sound("assignment2/assets/ring.mp3") 


    pause_button = pygame.Rect(10, 50, 100, 50)


    background_image = pygame.image.load('assignment2/assets/background.png').convert_alpha()


    background_rect = background_image.get_rect()


    if background_rect.width != SCREEN_WIDTH or background_rect.height != SCREEN_HEIGHT:
        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    


    background_image.set_alpha(128)  


    paused = False
    pause_time = 0


    while running:
        # Draw background
        screen.blit(background_image, (0, 0))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if pause_button.collidepoint(pos):
                    if not paused:
                        pygame.mixer.music.pause()  
                        pause_time = time.time()
                        paused = True
                        result = show_pause_menu()
                        if result == "continue":
                            pygame.mixer.music.unpause()  
                            paused = False
                            start_time += time.time() - pause_time
                        elif result == True:
                            running = False
                        elif result == False:
                            running = False
                else:
                    click_time = time.time()
                    for note in notes:
                        if note.is_clicked(click_time, pos):
                            feedback = note.get_feedback()
                            if feedback == "Great":
                                score += 3
                                feedback_text = "Great!"  
                                feedback_time = time.time()  
                            # Play click sound
                            click_sound.play()
                            print(feedback)
        
        # Draw pause button
        pause_button = pygame.Rect(10, 50, 100, 50)
        pause_image = pygame.image.load('assignment2/assets/btn_pause.jpg')
        screen.blit(pause_image, (pause_button.x, pause_button.y))
        


        # Generate notes
        current_time = time.time() - start_time
        if not paused and next_beat_index < len(beat_times) and current_time >= beat_times[next_beat_index]:
            x = random.randint(NOTE_RADIUS, SCREEN_WIDTH - NOTE_RADIUS)
            while x < 120:  
                x = random.randint(NOTE_RADIUS, SCREEN_WIDTH - NOTE_RADIUS)
            y = random.randint(NOTE_RADIUS, SCREEN_HEIGHT - NOTE_RADIUS)
            while y < 100:  
                y = random.randint(NOTE_RADIUS, SCREEN_HEIGHT - NOTE_RADIUS)


            appear_time = time.time()
            notes.append(Note(x, y, appear_time))
            next_beat_index += 1


        # Draw and update notes
        for note in notes:
            note.draw()


        # Remove expired and clicked notes
        notes = [note for note in notes if time.time() - note.appear_time < NOTE_LIFETIME and note.hit_time is None]
        
        # Draw feedback
        if feedback_text != "":
            feedback_surface = FONT.render(feedback_text, True, WHITE)
            screen.blit(feedback_surface, (SCREEN_WIDTH // 2 - feedback_surface.get_width() // 2, (SCREEN_HEIGHT // 2 - feedback_surface.get_height() // 2) + 200))
            if time.time() - feedback_time > 0.5:  
                feedback_text = ""
        
        pygame.display.flip()
        clock.tick(60)


        # Display score
        score_text = FONT.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))



        # Check if audio is finished
        if not pygame.mixer.music.get_busy():
            running = False
            


    if show_summary():
        main_game_loop()


# Main game loop
def main():
    if show_start_menu():
        main_game_loop()


if __name__ == "__main__":
    main()
    pygame.quit