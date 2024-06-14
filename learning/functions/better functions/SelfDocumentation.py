
def get_users_bad():
    users: dict[int, str] = {1: 'Bob', 2: 'Jeff', 3: 'Tom'}
    return users

def get_users_good() -> dict[int, str]:
    #doing """""" allows you to give information when hovering over this function later on
    """Retrieves the values and usernames from a database as a dict

    Returns:
        dict[int, str]: A dictionry of users
    """
    users: dict[int, str] = {1: 'Bob', 2: 'Jeff', 3: 'Tom'}
    return users

def display_users(users: dict[int, str]) -> None:
    """Outputs users from a dictionary in a nice format

    Args:
        users (dict[int, str]): A dictionary of users
    """
    for key, user_name in users.items():
        print(key, user_name, sep = ': ')
    


def main() -> None:
    #hover over get_users_good()
    get_users_good()
    users: dict[int, str] = get_users_good()
    display_users(users)

if __name__ == '__main__':
    main()