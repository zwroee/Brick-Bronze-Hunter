#Messing around w a gui output first time please forgive the spagetti here

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
import time

from PIL import Image, ImageTk

from loop_logic import start
import os
import shutil
from config_handler import set_info_in_config
import webbrowser

import threading


def validate_number_input(P):
    if P == "" or P.isdigit():
        return True
    try:
        float(P)
        return True
    except ValueError:
        return False

def countdown(timer, callback):
    """Countdown function that updates the timer label."""
    for t in range(timer, -1, -1):
        countdown_label.config(text=f"Starting in: {t} seconds", font="Courier 25 bold", foreground="red")
        root.update()
        time.sleep(1)
    
    threading.Thread(target=callback, daemon=True).start()

def setup_gui(config):

    """Set up the main window and widgets."""
    global root, countdown_label, vcmd
    root = tk.Tk()
    root.title("Pokemon Brick Bronze Auto Hunter")
    root.geometry("650x850")  # Set the window size to 600x400
    root.iconbitmap("icons/program_icon.ico")
    root.resizable(False, False)

    s = ttk.Style()
    COLOR_YELLOW = "#F5D442"           # accent
    COLOR_PURPLE = "#2D2D30"           # selected/tab background
    BACKGROUND_COLOR = "#1E1E1E"       # window background
    FOREGROUND_COLOR = "#E6E6E6"       # primary text

    root.configure(bg=BACKGROUND_COLOR)

    s.theme_create("yummy", parent="alt", settings={
    "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0], "background": BACKGROUND_COLOR }},
    "TNotebook.Tab": {
    "configure": {"padding": [5, 1], "background": "#252526", "foreground": FOREGROUND_COLOR},
    "map":       {"background": [("selected", COLOR_PURPLE)],
                   "foreground": [("selected", COLOR_YELLOW)],
                   "expand": [("selected", [1, 1, 1, 0])] } } } )
    
    s.theme_use("yummy")
    s.configure('TNotebook', background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)


    s.configure('TFrame', background=BACKGROUND_COLOR)
    s.configure('start.TButton', foreground=BACKGROUND_COLOR, background=COLOR_YELLOW, font=('Helvetica 20 bold'), padding=10)
    s.map('start.TButton', background=[('active', '#E6C200')], foreground=[('active', BACKGROUND_COLOR)])
    s.configure('TLabel', foreground=FOREGROUND_COLOR, background=BACKGROUND_COLOR, font=('Courier 12 bold'))
    s.configure('TEntry', fieldbackground="#2A2A2A", foreground=FOREGROUND_COLOR, insertcolor=FOREGROUND_COLOR, font=('Courier 20 bold'))
    s.configure('TCheckbutton', background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)

    
    vcmd = root.register(validate_number_input)

    # Create a Notebook widget (tabs)
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill='both')
################swsswssws#######################
    # Tab 1: Basic features
    basic_tab = ttk.Frame(notebook)
    notebook.add(basic_tab, text="Start")


    padx_input = 30
    pady_input = 5

    
# Label to display output

    #THIS IS THE LOGO HERE
    img = ImageTk.PhotoImage(Image.open("icons/program_logo.png"))
    label_logo = ttk.Label(basic_tab, image=img)
    label_logo.pack(padx=padx_input, pady=pady_input)

    label_blurb = ttk.Label(basic_tab, text="Welcome! Please go to the info tab for instructions!", font="Courier 13 bold")
    label_blurb.pack(padx=padx_input, pady=pady_input)

    label_countdown_time = ttk.Label(basic_tab, text="Start Countdown (Seconds):")
    label_countdown_time.pack(padx=padx_input, pady=pady_input, anchor="nw")
    #text box
    entry_countdown_time = ttk.Entry(basic_tab, validate="key", validatecommand=(vcmd, "%P"))
    entry_countdown_time.pack(padx=padx_input, pady=pady_input, anchor="nw")
    entry_countdown_time.insert(0, config.countdown_time)  # Pre-fill with a predetermined number

    label_key1 = ttk.Label(basic_tab, text="Key 1 (The first key that we use to move):")
    label_key1.pack(padx=padx_input, pady=pady_input, anchor="nw")

    entry_key1 = ttk.Entry(basic_tab, validate="key")
    entry_key1.pack(padx=padx_input, pady=pady_input, anchor="nw")
    entry_key1.insert(0, config.key_1)  # Pre-fill with a predetermined number

    label_key2 = ttk.Label(basic_tab, text="Key 2: (The second key that we use to move):")
    label_key2.pack(padx=padx_input, pady=pady_input, anchor="nw")

    entry_key2 = ttk.Entry(basic_tab, validate="key")
    entry_key2.pack(padx=padx_input, pady=pady_input, anchor="nw")
    entry_key2.insert(0, config.key_2)  # Pre-fill with a predetermined number

    label_hold_time = ttk.Label(basic_tab, text="Hold Time (How long in seconds we hold each key above):")
    label_hold_time.pack(padx=padx_input, pady=pady_input, anchor="nw")
    

    entry_hold_time = ttk.Entry(basic_tab, validate="key", validatecommand=(vcmd, "%P"))
    entry_hold_time.pack(padx=padx_input, pady=pady_input, anchor="nw")
    entry_hold_time.insert(0, int(config.hold_time))  # Pre-fill with a predetermined number

    # Label to display the countdown
    countdown_label = ttk.Label(basic_tab)
    countdown_label.pack(pady=10)
    
   ########################################################################################## 

    # Tab 2: Advanced features
    advanced_tab = ttk.Frame(notebook)
    notebook.add(advanced_tab, text="Advanced")

    label_adv_blurb = ttk.Label(advanced_tab, text="This is for advanced users. Use at your own risk!", font="Helvetica 15 bold")
    label_adv_blurb.pack(padx=padx_input, pady=pady_input)


    # Example advanced feature: An extra entry box
    advanced_label_precheck_threshold = ttk.Label(advanced_tab, text="Precheck Threshold:")
    advanced_label_precheck_threshold.pack(padx=padx_input, pady=pady_input)
    advanced_entry_precheck_threshold = ttk.Entry(advanced_tab, validate="key", validatecommand=(vcmd, "%P"))
    advanced_entry_precheck_threshold.pack(padx=padx_input, pady=pady_input)
    advanced_entry_precheck_threshold.insert(0, float(config.precheck_threshold))

    advanced_label_threshold = ttk.Label(advanced_tab, text="Threshold:")
    advanced_label_threshold.pack(padx=padx_input, pady=pady_input)
    advanced_entry_threshold = ttk.Entry(advanced_tab, validate="key", validatecommand=(vcmd, "%P"))
    advanced_entry_threshold.pack(padx=padx_input, pady=pady_input)
    advanced_entry_threshold.insert(0, float(config.threshold))  # Pre-fill with a predetermined number
    

    debug_var = tk.BooleanVar()
    #this doesn't work so its just there for show lol i will maybe get some config going later
    debug_button = ttk.Checkbutton(advanced_tab, variable=debug_var, text='Debug', onvalue=True, offvalue=False)
    debug_button.pack(padx=padx_input, pady=pady_input)

    # Calibrate Run button (capture mouse position and save)
    def calibrate_run_button_position():
        try:
            # 3-second delayed capture so user can hover over the Run button in Roblox
            countdown_window = tk.Toplevel(root)
            countdown_window.title("Calibration")
            countdown_window.configure(bg=BACKGROUND_COLOR)
            lbl = ttk.Label(countdown_window, text="Hover the mouse over RUN in Roblox...", font=('Helvetica 12 bold'))
            lbl.pack(padx=20, pady=10)
            timer_lbl = ttk.Label(countdown_window, text="Capturing in 3", font=('Helvetica 16 bold'))
            timer_lbl.pack(padx=20, pady=10)

            def do_capture():
                try:
                    import pyautogui as pg
                    x, y = pg.position()
                    set_info_in_config('config.txt', 'target_coordinates_x', str(x))
                    set_info_in_config('config.txt', 'target_coordinates_y', str(y))
                    config.target_coordinates = [x, y]
                    countdown_window.destroy()
                    messagebox.showinfo("Saved", f"Run button position saved: ({x}, {y})")
                except Exception as e:
                    countdown_window.destroy()
                    messagebox.showerror("Error", f"Failed to save position: {e}")

            def tick(count):
                if count <= 0:
                    do_capture()
                else:
                    timer_lbl.config(text=f"Capturing in {count}")
                    root.after(1000, tick, count - 1)

            # start countdown
            tick(3)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start calibration: {e}")

    calibrate_button = ttk.Button(advanced_tab, text="Calibrate Run Button (3s hover capture)", command=calibrate_run_button_position)
    calibrate_button.pack(padx=padx_input, pady=pady_input)

    # Test click
    def test_click_run():
        try:
            from auto_move import move_mouse
            move_mouse(config.target_coordinates)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to click: {e}")

    test_click_btn = ttk.Button(advanced_tab, text="Test Click RUN", command=test_click_run)
    test_click_btn.pack(padx=padx_input, pady=pady_input)

    # Discord webhook settings
    discord_label = ttk.Label(advanced_tab, text="Discord Webhook URL (optional):", font="Helvetica 12 bold")
    discord_label.pack(padx=padx_input, pady=pady_input)
    
    discord_entry = ttk.Entry(advanced_tab, width=60)
    discord_entry.pack(padx=padx_input, pady=pady_input)
    discord_entry.insert(0, config.discord_webhook_url)
    
    discord_help_label = ttk.Label(advanced_tab, text="Leave empty to disable Discord notifications", font="Helvetica 9 italic")
    discord_help_label.pack(padx=padx_input, pady=2)
    
    # Test webhook button
    def test_discord_webhook():
        from discord_webhook import DiscordWebhook
        webhook_url = discord_entry.get().strip()
        if webhook_url:
            webhook = DiscordWebhook(webhook_url)
            if webhook.test_webhook():
                messagebox.showinfo("Success", "Discord webhook test successful! Check your Discord server.")
            else:
                messagebox.showerror("Error", "Discord webhook test failed. Check your webhook URL.")
        else:
            messagebox.showwarning("Warning", "Please enter a Discord webhook URL first.")
    
    test_webhook_button = ttk.Button(advanced_tab, text="Test Discord Webhook", command=test_discord_webhook)
    test_webhook_button.pack(padx=padx_input, pady=pady_input)


    info_tab = ttk.Frame(notebook)
    notebook.add(info_tab, text="Info")

    label_info_text = ttk.Label(info_tab, text=startup_text(), font="Helvetica 10 bold")
    label_info_text.pack(padx=10, pady=10)

    # Clickable hyperlink to Project Pokémon sprites page
    def open_sprites_link(url):
        webbrowser.open(url)

    link_style = ttk.Style()
    link_style.configure('Link.TLabel', foreground='#4EA1F3', background=BACKGROUND_COLOR, font=('Helvetica 10 underline'))

    links = [
        ("Project Pokémon 3D Models: Generation 1", "https://projectpokemon.org/home/docs/spriteindex_148/3d-models-generation-1-pok%C3%A9mon-r90/"),
        ("Project Pokémon 3D Models: Generation 2", "https://projectpokemon.org/home/docs/spriteindex_148/3d-models-generation-2-pok%C3%A9mon-r91/"),
        ("Project Pokémon 3D Models: Generation 3", "https://projectpokemon.org/home/docs/spriteindex_148/3d-models-generation-3-pok%C3%A9mon-r92/"),
        ("Project Pokémon 3D Models: Generation 4", "https://projectpokemon.org/home/docs/spriteindex_148/3d-models-generation-4-pok%C3%A9mon-r93/"),
        ("Project Pokémon 3D Models: Generation 5", "https://projectpokemon.org/home/docs/spriteindex_148/3d-models-generation-5-pok%C3%A9mon-r94/"),
        ("Project Pokémon 3D Models: Generation 6", "https://projectpokemon.org/home/docs/spriteindex_148/3d-models-generation-6-pok%C3%A9mon-r95/"),
        ("Project Pokémon 3D Models: Generation 7", "https://projectpokemon.org/home/docs/spriteindex_148/3d-models-generation-7-pok%C3%A9mon-r96/"),
        ("Project Pokémon 3D Models: Generation 8", "https://projectpokemon.org/home/docs/spriteindex_148/3d-models-generation-8-pok%C3%A9mon-r123/")
    ]

    for text, url in links:
        lbl = ttk.Label(info_tab, text=text, style='Link.TLabel', cursor='hand2')
        lbl.bind("<Button-1>", lambda e, u=url: open_sprites_link(u))
        lbl.pack(padx=10, pady=2, anchor='w')

#########################################################################################################
######## IDK HOW THIS WORKS I GOT IT FROM ONLINE BUT IT THOUGHT IT WAS PRETTY BUT IF SOMETHING ##########
################### BREAKS BECAUSE OF THIS JUST THROW IT AWAY ITS JUST FOR DECORATION ###################
#########################################################################################################
                                                                                                        #
    animation_job = {"id": None}                                                                       #

    def stop_animation():                                                                                #
        if animation_job["id"] is not None:                                                             #
            try:                                                                                         #
                root.after_cancel(animation_job["id"])                                                  #
            except Exception:                                                                            #
                pass                                                                                     #
            finally:                                                                                     #
                animation_job["id"] = None                                                               #

    def animate_gif(label, frames, delay, idx=0):                                                       #
        if not label.winfo_exists() or not root.winfo_exists():                                         #
            stop_animation()                                                                            #
            return                                                                                      #
        try:                                                                                            #
            frame = frames[idx]                                                                         #
            gif_img = ImageTk.PhotoImage(frame)                                                         #
            label.config(image=gif_img)                                                                 #
            label.image = gif_img                                                                       #
        except Exception:                                                                               #
            # If a frame fails to render, skip to next                                                 #
            pass                                                                                        #
        animation_job["id"] = root.after(delay, animate_gif, label, frames, delay, (idx + 1) % len(frames))#
                                                                                                        #
    def load_gif(path):                                                                                 #
        gif = Image.open(path)                                                                          #
        frames = []                                                                                     #
        try:                                                                                            #
            for frame in range(gif.n_frames):                                                           #
                gif.seek(frame)                                                                         #
                frames.append(gif.copy().convert("RGBA"))                                              #
        except Exception:                                                                               #
            pass                                                                                        #
        delay = int(1000 / (gif.info.get("duration", 10) or 10))                                       #
        return frames, delay                                                                            #

    def display_preview_for_path(path):                                                                 #
        stop_animation()                                                                                #
        try:                                                                                            #
            img = Image.open(path)                                                                      #
            if getattr(img, "is_animated", False) and getattr(img, "n_frames", 1) > 1:                #
                frames, delay = load_gif(path)                                                          #
                if frames:                                                                              #
                    animate_gif(gif_label, frames, delay)                                              #
            else:                                                                                       #
                static_img = ImageTk.PhotoImage(img.convert("RGBA"))                                   #
                gif_label.config(image=static_img)                                                      #
                gif_label.image = static_img                                                            #
            # update filename label                                                                     #
            try:                                                                                        #
                import os                                                                               #
                name = os.path.splitext(os.path.basename(path))[0]                                      #
                name = name.replace('_', ' ').title()                                                   #
                gif_filename_label.config(text=name)                                                    #
            except Exception:                                                                           #
                gif_filename_label.config(text="")                                                     #
        except Exception:                                                                               #
            pass                                                                                        #

    # Display current fight target dynamically (uses preview area)
    def display_current_enemy(enemy_image_path):
        display_preview_for_path(enemy_image_path)
                                                                                                        #
    gif_name_label = ttk.Label(basic_tab, text="HUNTING FOR", font='Courier 15 bold')                   #
    gif_name_label.pack(padx=padx_input, pady=pady_input, anchor="nw")                                  #
                                                                                                        #
    gif_label = ttk.Label(basic_tab)                                                                    #
    gif_label.pack(padx=padx_input * 2, pady=(pady_input, 2), anchor="nw")                              #
    gif_filename_label = ttk.Label(basic_tab, text="", font='Courier 12 bold')                         #
    gif_filename_label.pack(padx=padx_input * 2, pady=(0, pady_input), anchor="nw")                     #
                                                                                                        #
    try:                                                                                                #
        display_preview_for_path(config.img_dir)                                                        #
    except Exception as e:                                                                              #
        pass                                                                                            #

    def on_close():                                                                                     #
        stop_animation()                                                                                #
        try:                                                                                            #
            root.destroy()                                                                              #
        except Exception:                                                                               #
            pass                                                                                        #
    root.protocol("WM_DELETE_WINDOW", on_close)                                                         #
                                                                                                        #
    def choose_image():                                                                                  #
        try:                                                                                             #
            filetypes = [("Images", "*.gif *.webp *.png *.jpg *.jpeg *.tiff *.tif")]                    #
            chosen = filedialog.askopenfilename(title="Select Pokemon image",                           #
                                               initialdir="image_folder",                               #
                                               filetypes=filetypes)                                      #
            if not chosen:                                                                              #
                return                                                                                  #
            os.makedirs("image_folder", exist_ok=True)                                                 #
            dest_name = os.path.basename(chosen)                                                        #
            dest_path = os.path.join("image_folder", dest_name)                                        #

            # Ensure only the selected image exists in image_folder                                     #
            chosen_in_folder = os.path.abspath(chosen).startswith(os.path.abspath("image_folder"))      #
            for f in os.listdir("image_folder"):                                                       #
                fp = os.path.join("image_folder", f)                                                   #
                if os.path.isfile(fp):                                                                  #
                    if chosen_in_folder and os.path.abspath(fp) == os.path.abspath(chosen):             #
                        continue                                                                         #
                    try:                                                                                #
                        os.remove(fp)                                                                   #
                    except Exception:                                                                   #
                        pass                                                                            #

            if not chosen_in_folder:                                                                    #
                shutil.copy2(chosen, dest_path)                                                         #
            else:                                                                                       #
                dest_path = chosen                                                                      #
            # persist to config                                                                            #
            set_info_in_config('config.txt', 'folder_path', './image_folder')                           #
            # update runtime config                                                                        #
            config.img_dir = dest_path                                                                   #
            # refresh preview to show selected target under "HUNTING FOR"                                  #
            display_preview_for_path(config.img_dir)                                                     #
            messagebox.showinfo("Target Updated", "Target image updated successfully.")                 #
        except Exception as e:                                                                           #
            messagebox.showerror("Error", f"Failed to set image: {e}")                                  #
                                                                                                        #
    choose_button = ttk.Button(basic_tab, text="Change Target Image", command=choose_image)             #
    choose_button.pack(padx=padx_input, pady=pady_input, anchor="nw")                                   #
#########################################################################################################

    #Gets ball rolling, does try catch on countodnw, if fails, its because of a bad output so it stops and sends message box
    def start_countdown():
        try:
            # disable start button visually and functionally
            start_btn_canvas.unbind("<Button-1>")
            for item in start_btn_parts:
                start_btn_canvas.itemconfig(item, fill="#8A7E1A")
            start_btn_canvas.itemconfig(start_btn_text, fill="#3A3A3A")

            #sets 
            config.countdown_timer = int(entry_countdown_time.get()) 
            config.key_1 = entry_key1.get()
            config.key_2 = entry_key2.get()
            config.hold_time = int(entry_hold_time.get())

            config.threshold = float(advanced_entry_threshold.get())
            config.discord_webhook_url = discord_entry.get()

            config.debug = debug_var.get()

            print("THRES: ", config.threshold)
            print("DEBUG: ", config.debug)


            countdown(config.countdown_timer, on_countdown_complete)
        except ValueError:
            messagebox.showerror("Invalid Input", " Invalid Input: Please double check your inputs and try again")

    #should be running on it's own thread
    def on_countdown_complete():

        #Calls START and loops forever
        label_start = ttk.Label(basic_tab, text="RUNNING", font="Courier 25 bold", foreground="red")
        label_start.pack(padx=10, pady=10)

        # Send startup notification to Discord
        try:
            from discord_webhook import DiscordWebhook
            avatar_url = getattr(config, 'discord_avatar_url', '') if hasattr(config, 'discord_avatar_url') else ''
            discord_webhook = DiscordWebhook(config.discord_webhook_url, avatar_url=avatar_url)
            discord_webhook.send_startup_notification()
        except Exception as e:
            print(f"Failed to send Discord startup notification: {e}")
        
        while True:
            result = start(config)
            if result is True:
                # target found: stop loop and visually disable start button already done
                break

    # Rounded-rectangle Start button using Canvas
    def draw_round_rect(canvas, x1, y1, x2, y2, r, **kwargs):
        items = []
        items.append(canvas.create_arc(x1, y1, x1 + 2*r, y1 + 2*r, start=90, extent=90, style='pieslice', **kwargs))
        items.append(canvas.create_arc(x2 - 2*r, y1, x2, y1 + 2*r, start=0, extent=90, style='pieslice', **kwargs))
        items.append(canvas.create_arc(x2 - 2*r, y2 - 2*r, x2, y2, start=270, extent=90, style='pieslice', **kwargs))
        items.append(canvas.create_arc(x1, y2 - 2*r, x1 + 2*r, y2, start=180, extent=90, style='pieslice', **kwargs))
        items.append(canvas.create_rectangle(x1 + r, y1, x2 - r, y2, **kwargs))
        items.append(canvas.create_rectangle(x1, y1 + r, x2, y2 - r, **kwargs))
        return items

    start_btn_canvas = tk.Canvas(basic_tab, width=260, height=120, highlightthickness=0, bg=BACKGROUND_COLOR)
    start_btn_canvas.pack(pady=10)
    start_btn_parts = draw_round_rect(start_btn_canvas, 10, 20, 250, 100, 24, fill=COLOR_YELLOW, outline=COLOR_YELLOW, width=0)
    start_btn_text = start_btn_canvas.create_text(130, 60, text="START", fill=BACKGROUND_COLOR, font=('Helvetica 24 bold'))

    def on_start_hover(event):
        for item in start_btn_parts:
            start_btn_canvas.itemconfig(item, fill="#E6C200")

    def on_start_leave(event):
        for item in start_btn_parts:
            start_btn_canvas.itemconfig(item, fill=COLOR_YELLOW)

    start_btn_canvas.bind("<Enter>", on_start_hover)
    start_btn_canvas.bind("<Leave>", on_start_leave)
    start_btn_canvas.bind("<Button-1>", lambda e: start_countdown())
    start_btn_canvas.configure(cursor='hand2')

    root.mainloop()



def startup_text():

    return """
    This Program is an auto pokemon finder for Pokemon Brick Bronze in Roblox.
    This program takes over and uses image recognition and auto key movements to automate
    Pokemon Hunting. This program can also be used to find shinys if you want.
    
    Quick Start Instructions:
    
        1. please Open Roblox and head to the tall grass 
            where you intend to do your shiny hunting with ample space to move around
        2. Please find the pokemon you are looking for from the links below in this tab.
           Save As and store the pokemon in the image_folder (or use Change Target Image).
        
        3. Hit Start and leave your computer on!
            Now you are free to leave the computer, and let it do its thing.
            When the program finds a match it will 'idle' to keep you connected, however 
            please don't leave this program on for hours as that has not been tested.

        Other Notes:

        This program only works for 16x9 monitors so no CRTS or ultrawide screens as I don't have
        those.

        I have a general "threshold" that works on most pokemon, if you are having trouble with
        false negatives or positives, please bring it down and check with the debug function.

        In the Advanced section, you have a threshold, which is 0.3 by standard. If you are having
        false positives (saying there is a pokemon match when there is not), bring it down by 
        dividing in half until you are not. If you are having false negatives (missing a match),
        double the threshold until you get a match. 

        If you want new defaults, edit on config.txt. Please be careful and keep the format I put.

        Discord Notifications:
        
        You can now get Discord notifications when Pokemon are found! To set this up:
        
        1. Go to your Discord server
        2. Click Server Settings > Integrations > Webhooks
        3. Click "Create Webhook"
        4. Copy the webhook URL
        5. Paste it in the Advanced tab under "Discord Webhook URL"
        6. Click "Test Discord Webhook" to verify it works
        
        The bot will send notifications when:
        - The hunting starts
        - A Pokemon match is found
        
        Also, please be careful doing this, as you can get kicked for being a bot. I know because
        it happened to me once already :(

        If you are doing shiny hunting, 0.3 seems to work just fine for most things, however this 
        program has only caught shinys that are different color shade than their non-shiny 
        counterparts.It sometimes struggles with shinys like Pidgey which variation is very slight. 
        Please test before usage as while this works well on my machine, I cannot vouch for yours.

        I tried to make it dummy proof but if you manage to break it, tell me how!

        https://github.com/jaloaguero
        jaloaguero@gmail.com
        
        """