

from image_recognition import compare_images, get_text_from_screenshot, is_run_button_visible
from auto_move import move_mouse, press_keys, idle_game, idle_for, click_run_button
from discord_webhook import DiscordWebhook

def start(config):
        # Initialize Discord webhook if configured
        discord_webhook = DiscordWebhook(config.discord_webhook_url)
        
        print("Pressing key: ",config.key_1)
        press_keys(config.key_1,config.hold_time)
        print("Pressing key: ", config.key_2)
        press_keys(config.key_2,config.hold_time)

        print("Chekcing if we are in battle...")
        # Prefer OCR; if unavailable, fall back to visual Run button detection
        in_battle = get_text_from_screenshot(config.text_coords, config.debug)
        if in_battle is False:
            in_battle = is_run_button_visible(config.target_coordinates)

        if in_battle == True:

            print("We are in battle. Looking for pokemon match on screen.")
            pokemon_found = compare_images(config.img_dir,config.precheck_threshold, config.threshold, config.img_scale_percent, config.debug)
            # Second-chance verification to prevent fleeing from correct Pokemon
            if pokemon_found is False:
                try:
                    alt_threshold = min(1.0, config.threshold * 1.5)
                    for scale in [config.img_scale_percent, max(50, config.img_scale_percent - 50), config.img_scale_percent + 50]:
                        recheck = compare_images(config.img_dir, config.precheck_threshold, alt_threshold, scale, config.debug)
                        if recheck is True:
                            pokemon_found = True
                            break
                except Exception:
                    pass
            if pokemon_found == False:
                print("Pokemon match not found, moving mouse to flee...")
                try:
                    click_run_button(config.target_coordinates)
                except Exception:
                    move_mouse(config.target_coordinates)
                return False
            else:
                print("Pokemon match found! Idling game...")
                
                # Send Discord notification
                try:
                    # Extract Pokemon name from image file path
                    import os
                    pokemon_name = os.path.splitext(os.path.basename(config.img_dir))[0]
                    pokemon_name = pokemon_name.replace('_', ' ').title()
                    
                    discord_webhook.send_pokemon_found_notification(pokemon_name)
                except Exception as e:
                    print(f"Failed to send Discord notification: {e}")
                # Idle for a short period to avoid AFK, then stop automation
                try:
                    idle_for(60)  # idle ~1 minute to avoid AFK
                except Exception:
                    pass
                return True
        else:
            print("Either not in battle, or currently entering battle...")
            return False

