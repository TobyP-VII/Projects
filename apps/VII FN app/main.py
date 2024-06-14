
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
# from kivy.config import Config
from check_shop import check_shop

check_shop()

# Config.set('graphics', 'width', '406')
# Config.set('graphics', 'height', '720')

class MainWindow (Screen):
    pass

class ShopWindow (Screen):
    pass

class StatsWindow (Screen):
    pass

class MapWindow (Screen):
    pass

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file('viiapp.kv')

class ViiApp(App):
    def build(self):
        return kv

    
if __name__ == '__main__':
    ViiApp().run()