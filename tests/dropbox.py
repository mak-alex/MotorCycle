# Include the Dropbox SDK
import dropbox
dbx = dropbox.Dropbox('pzTH_pckjxAAAAAAAAAADZgB3-ofGXqNJGMjMiDyk8E')
print(dbx.users_get_current_account())
