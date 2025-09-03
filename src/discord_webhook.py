"""
Discord Webhook Integration for Pokemon Brick Bronze Auto Hunter
Handles sending notifications to Discord when Pokemon are found
"""

import requests
import json
import time
from datetime import datetime
import os

class DiscordWebhook:
    def __init__(self, webhook_url=None, avatar_url: str = ""):
        """
        Initialize Discord webhook handler
        
        Args:
            webhook_url (str): Discord webhook URL. If None or empty, notifications are disabled
        """
        self.webhook_url = webhook_url
        self.enabled = bool(webhook_url and webhook_url.strip())
        self.avatar_url = avatar_url.strip() if avatar_url else ""
        
    def send_pokemon_found_notification(self, pokemon_name="Unknown Pokemon", screenshot_path=None):
        """
        Send a notification to Discord when a Pokemon is found
        
        Args:
            pokemon_name (str): Name of the Pokemon found
            screenshot_path (str): Optional path to screenshot to attach
        """
        if not self.enabled:
            print("Discord notifications are disabled (no webhook URL configured)")
            return False
            
        try:
            # Create the embed message
            embed = {
                "title": "🎉 Pokemon Found!",
                "description": f"**{pokemon_name}** has been detected!",
                "color": 0x00ff00,  # Green color
                "timestamp": datetime.utcnow().isoformat(),
                "fields": [
                    {
                        "name": "🕐 Time Found",
                        "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "inline": True
                    },
                    {
                        "name": "🎮 Game",
                        "value": "Pokemon Brick Bronze",
                        "inline": True
                    }
                ],
                "footer": {
                    "text": "Pokemon Brick Bronze Auto Hunter"
                }
            }
            
            # Prepare the payload
            payload = {
                "username": "Pokemon Hunter Bot",
                "avatar_url": self.avatar_url if self.avatar_url else None,
                "embeds": [embed]
            }
            # Remove None keys
            payload = {k: v for k, v in payload.items() if v is not None}
            
            # Add screenshot if provided and file exists
            files = {}
            # Add screenshot if provided
            if screenshot_path and os.path.exists(screenshot_path):
                try:
                    files['file'] = (os.path.basename(screenshot_path), open(screenshot_path, 'rb'), 'image/png')
                except Exception as e:
                    print(f"Warning: Could not attach screenshot: {e}")
            
            # Send the webhook
            response = requests.post(
                self.webhook_url,
                json=payload,
                files=files,
                timeout=10
            )
            
            # Close file if it was opened
            try:
                if 'file' in files:
                    files['file'][1].close()
                if 'avatar' in files:
                    files['avatar'][1].close()
            except Exception:
                pass
            
            if response.status_code == 204:
                print("✅ Discord notification sent successfully!")
                return True
            else:
                print(f"❌ Failed to send Discord notification. Status: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except requests.exceptions.Timeout:
            print("❌ Discord webhook request timed out")
            return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Discord webhook request failed: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error sending Discord notification: {e}")
            return False
    
    def send_startup_notification(self):
        """
        Send a notification when the bot starts hunting
        """
        if not self.enabled:
            return False
            
        try:
            embed = {
                "title": "🚀 Pokemon Hunter Started",
                "description": "The Pokemon Brick Bronze Auto Hunter has started searching!",
                "color": 0x0099ff,  # Blue color
                "timestamp": datetime.utcnow().isoformat(),
                "fields": [
                    {
                        "name": "🕐 Start Time",
                        "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "inline": True
                    }
                ],
                "footer": {
                    "text": "Pokemon Brick Bronze Auto Hunter"
                }
            }
            
            payload = {
                "username": "Pokemon Hunter Bot",
                "avatar_url": self.avatar_url if self.avatar_url else None,
                "embeds": [embed]
            }
            payload = {k: v for k, v in payload.items() if v is not None}
            
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            
            if response.status_code == 204:
                print("✅ Discord startup notification sent!")
                return True
            else:
                if response.status_code == 401 or response.status_code == 404:
                    print("❌ Failed to send startup notification: Invalid or deleted webhook URL. Make sure you pasted the full URL from Discord (Format: https://discord.com/api/webhooks/ID/TOKEN)")
                else:
                    print(f"❌ Failed to send startup notification. Status: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error sending startup notification: {e}")
            return False
    
    def test_webhook(self):
        """
        Test the webhook connection
        """
        if not self.enabled:
            print("❌ Discord webhook is not configured")
            return False
            
        try:
            embed = {
                "title": "🧪 Webhook Test",
                "description": "This is a test message to verify Discord webhook integration is working!",
                "color": 0xff9900,  # Orange color
                "timestamp": datetime.utcnow().isoformat(),
                "footer": {
                    "text": "Pokemon Brick Bronze Auto Hunter - Test Message"
                }
            }
            
            payload = {
                "username": "Pokemon Hunter Bot",
                "embeds": [embed]
            }
            
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            
            if response.status_code == 204:
                print("✅ Discord webhook test successful!")
                return True
            else:
                if response.status_code == 401 or response.status_code == 404:
                    print("❌ Discord webhook test failed: Invalid or deleted webhook URL. Recreate a webhook in Discord and copy the entire URL.")
                else:
                    print(f"❌ Discord webhook test failed. Status: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Discord webhook test error: {e}")
            return False
