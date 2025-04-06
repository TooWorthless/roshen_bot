from db.database import init_db
from handlers import main

if __name__ == '__main__':
    init_db()
    print("RoshenBot is running...")
    main.bot.infinity_polling()