#Enum is used to set names bound to unique values
from enum import Enum

#Enum is used in a class to pair names with values
class Quality(Enum):
    #type: ignore is used for if there is something that has been imported just so it doesnt keep showing errors when in reality it is working
    low: int = 480 #type: ignore
    medium: int = 1080 #type: ignore
    high: int = 1440 #type: ignore

class Privacy(Enum):
    private: str = 'Private' #type: ignore
    unlisted: str = 'Unlisted' #type: ignore
    public: str = 'Public' #type: ignore

#putting a * will make everything after it to require the keyword so it's more explicit
def upload(file: str, *, quality: Quality, privacy: Privacy) -> None:
    print(f'Uploading: "{file}" in {quality.value}p ({privacy.value})')
    
def main() -> None:
    #due to the * in upload(), "quality" and "privacy" are both required
    upload('file_name.mp4', quality = Quality.low, privacy = Privacy.private)
    
if __name__ == '__main__':
    main()
    