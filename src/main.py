from gui import setup_gui
from config_init import init_config

def main():
    #creates class that setup_gui needs, then calls setup_gui. basically main.py just exists to kinda "start" the program.
    config = init_config()
    setup_gui(config)
       
if __name__ == '__main__':
    main()