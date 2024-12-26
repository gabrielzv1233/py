from discordinfo import get_profile

token = input("Discord user token (must be from a user that is in a server or DMs with the owner of the used Discord ID): ")
user_id = input("Enter the user ID: ")

profile_data, status = get_profile(token, user_id)

if status == 1:
    avatar = profile_data.get('user', {}).get('avatar')
    
    if avatar:
        avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar}.webp"
        print("\nAvatar URL:")
        print(avatar_url)
    else:
        print("\nNo avatar found for this user.")
else:
    print("\nFailed to retrieve profile data.")
