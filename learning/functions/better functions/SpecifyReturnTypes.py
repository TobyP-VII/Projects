
#bad - can get confusing on what is being returned
def get_users_bad():
    users: dict[int, str] = {1: 'Bob', 2: 'Jeff', 3: 'Tom'}
    return users

#good - give context on what is being returned
def get_users_good() -> dict[int, str]:
    users: dict[int, str] = {1: 'Bob', 2: 'Jeff', 3: 'Tom'}
    return users

#self documentation
#return None as all this needs to do is run, not assigned to anything
def display_users(users: dict[int, str]) -> None:
    for key, user_name in users.items():
        print(key, user_name, sep = ': ')
    


def main() -> None:
    get_users_good()
    users: dict[int, str] = get_users_good()
    display_users(users)

if __name__ == '__main__':
    main()