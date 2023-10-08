import pygame 
from pygame import mixer
from  random import choice 
import textwrap
import time 

pygame.init()
mixer.init()

screen_width=800
screen_length=600

screen=pygame.display.set_mode((800,600))
white=(255,255,255)
red=(255,0,0)
black=(0,0,0)
green=(0,255,0)
blue=(0,0,255)
cyan=(0, 255, 255)
transparent_green = (153, 255, 153)
transparent_color = (0, 0, 0, 0)


rect_x=0
rect_y=20


# font file load 
file_name="cmunbtl.ttf"
font_path=f"cmu/{file_name}"
font_size=40
font = pygame.font.Font(font_path, font_size)

## store text coordinates font , rect , letter
text_coordinates=[]

button_width = 200
button_height = 50
button_color = (0, 128, 255)
button_hover_color = (0, 0, 255)
text_color = (255, 255, 255)
button_text = "START."
button_rect = pygame.Rect((screen_width - button_width) // 2, (screen_length - button_height) // 2, button_width, button_height)

# play sound of wav file
def play_wav_file_with_no_lag(filename):
  """
  Plays a WAV file with no lag using the `pygame.mixer` module.
  Args:
    filename: The path to the WAV file.
  """
  # Initialize Pygame
  # Load the WAV file.
  sound = pygame.mixer.Sound(filename)
  # Play the WAV file.
  sound.play()



##it render the start button on the screen begining 
def render_button():
   # Create a surface for the button with a filled rectangle
   button_surface = pygame.Surface((button_width, button_height))
   button_surface.fill(button_color)

   # Render the text on the button surface
   text_surface = font.render(button_text, True, text_color)
   text_rect = text_surface.get_rect(center=button_surface.get_rect().center)

   # Blit (draw) the text onto the button surface
   button_surface.blit(text_surface, text_rect)

   # Get the rectangle of the button surface
   button_rect = button_surface.get_rect()
   
   return button_surface, button_rect

## It's text pointer that move when you type 
def text_pointer(coordinates):
   """Draws a transparent rectangle at the given coordinates."""
   # Create a new surface with a per-pixel alpha format.
   transparent_surface = pygame.Surface(coordinates.size, pygame.SRCALPHA)
   # Draw the rectangle on the new surface.
   #(0, 255, 0)
   transparent_surface.fill(cyan)
   # Set the alpha value of the new surface.
   pointer_brightness=128
   transparent_surface.set_alpha(pointer_brightness)
   # Blit the new surface onto the screen.
   screen.blit(transparent_surface, coordinates)
   return

#it palce the text according to screen size
def manage_text_placing(text,max_width):
   rapped_word = textwrap.fill(text, width=max_width)
   return rapped_word

#it makes a render  text for  screen 
def text_render(text):
   global text_coordinates
   text_width = font.render(text[0], True, (255, 255, 255)).get_width()
   max_width=screen_width//text_width+1
   texts=manage_text_placing(text,max_width)
   
   rect_width=0
   rect_height=0
   x=rect_x
   y=rect_y
   for letter in texts:
      x += rect_width + 19  # Add some spacing between rectangles
      #if x >= screen_width-10:
      if letter=="\n":
         y+= rect_height + 40
         x=rect_x
         continue
         #letter=' '
      
      text_surface=font.render(letter,True,white)
      text_rect = text_surface.get_rect()
      text_rect.center = (x,y)
      
      text_coordinates.append([text_surface,text_rect,letter])
      rec_width = text_rect.width
      rec_height = text_rect.height

   return 


## it renders the typing text on screen 
def render_on_scrren(text_coordinates):
   for text_surface , text_rect , letter in text_coordinates:
      screen.blit(text_surface, text_rect)
   return 


## it  calculate and renders the typing speed on the screen 
def render_typing_speed(timer,text):
   print(timer)
   if timer > 0 :
      length= len(text.split())
      typing_speed = length/(timer/60000)
   else:
      typing_speed=0
   
   speed_text=f"T-s: {round(typing_speed,2)} WPM"
   
   speed_font=font.render(speed_text,True,green)
   speed_x , speed_y = (screen_width - button_width) // 2, (screen_length - button_height) // 2+100
   
   screen.blit(speed_font, (speed_x,speed_y))
   return 
# it calculate accuracy and render it on screen
def render_accuracy(text,right_characters):
   if len(text)>0 and right_characters>0:
      accuracy = (right_characters/len(text))*100
   else:
      accuracy=0
   speed_text=f"Acc: {round(accuracy,2)}%"
   acc_font=font.render(speed_text,True,green)
   acc_x , acc_y = (screen_width - button_width) // 2, (screen_length - button_height) // 2+200
   screen.blit(acc_font, (acc_x,acc_y))
   return 

## load typing data 
def load_text_file(filepath):
   lines = []
   with open(filepath, 'r') as file:
      for line in file:
         lines.append(line.rstrip())  # Remove trailing newline characters and add to the list
   return lines
game=True
typing_started=False 
FPS=60
screen=pygame.display.set_mode((800,600))
clock=pygame.time.Clock()
len_count=0
start_time=end_time=0
typing_data=load_text_file('typing_set/content.txt')
typed_text=''
text=''
correct_text=0
while game:
   clock.tick(FPS)
   screen.fill(black)
   # Check for the Shift and Caps Lock key modifiers
   shift_active = pygame.key.get_mods() & pygame.KMOD_SHIFT
   caps_lock_active = pygame.key.get_mods() & pygame.KMOD_CAPS

   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         game = False
      elif event.type == pygame.KEYDOWN:
         # Check if the pressed key is a printable ASCII character
         if event.key >= 32 and event.key <= 126 and len_count < len(text_coordinates) and typing_started==True:
            user_input = chr(event.key)
            if caps_lock_active or shift_active:
               user_input=user_input.upper()
            typed_text+=user_input
            text_rec=text_coordinates[len_count][1]
            cur_text=text_coordinates[len_count][2]

            #print(cur_text,user_input)
            if cur_text == user_input:
               play_wav_file_with_no_lag("sound/light_click.wav")
               text_coordinates[len_count][0]=font.render(cur_text,True,green)
               correct_text+=1
            #text_pointer(text_rec)
            else:
               play_wav_file_with_no_lag("sound/fail_click.wav")
               text_coordinates[len_count][0]=font.render(cur_text,True,red)
            len_count+=1
            #print(len_count)
            #render_on_scrren(text_coordinates)
      # whne start buttong is clicked intialize everything again  
      elif event.type == pygame.MOUSEBUTTONDOWN and typing_started==False:
         if button_rect.collidepoint(event.pos):
            ## randomly choose text from text file to type
            text=choice(typing_data)
            #text="The quick brown fox jumps over the lazy dog are you feelling it"
            # empty the text_coordinates 
            text_coordinates=[]
            #true the typing 
            typing_started=True
            # start the timer 
            # Get the current time in milliseconds
            start_time = pygame.time.get_ticks()
            #prev_time = time.perf_counter()
            # intialize current lenght which is typed to 0
            len_count=0
            # total correct text is 0
            correct_text=0
            #total typed text is empty 
            typed_text=''
            
            text_render(text)
            
   # if user typed the text to give text length reset the typing
   if len_count > len(text_coordinates)-1 and len(text_coordinates)>0:
      #print("reached the limit")
      #print(len_count)
      typing_started=False
      len_count=0
      # Get the current time in milliseconds
      end_time = pygame.time.get_ticks()
      #current_time=time.perf_counter()
   ## if typing started render the typing text and text pointer on scrren  
   if typing_started:
      render_on_scrren(text_coordinates)
      #
      text_pointer(text_coordinates[len_count][1])
   else:
      button_surface , botton_rect = render_button()
      screen.blit(button_surface,button_rect)
      # calculating time ussing time counter 
      elapsed_time = end_time - start_time
      #print(elapsed_time)
      ## pass time to claculate typing speed 
      render_typing_speed(elapsed_time , typed_text)
      ## pass text and correct text to calculate accuracy of typing
      render_accuracy(text,correct_text)
      
   pygame.display.flip()
   clock.tick(60)
