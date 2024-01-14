
class Settings:
    music_on: int = 1
    refresh_freq: int = 60

    @classmethod
    def display_settings(cls):
        pass

    @classmethod
    def get_music_setting(cls):
        return cls.music_on

    @classmethod
    def change_music_setting(cls):
        cls.music_on = 1 - cls.music_on
