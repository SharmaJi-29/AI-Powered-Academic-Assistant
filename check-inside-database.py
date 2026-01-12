if __name__ == "__main__":
    from database import get_all_users
    users = get_all_users()
    for user in users:
        print(user)