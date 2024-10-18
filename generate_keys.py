import bcrypt
hashed_pw = bcrypt.hashpw("intel123!".encode('utf-8'), bcrypt.gensalt())
print(hashed_pw)