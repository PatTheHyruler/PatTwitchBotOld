# PatTwitchBot

Twitch bot made for my own channel  
Use at your own risk

### Alembic stuff
#### Generate database migration
    alembic revision --autogenerate -m "Change message"
#### Run migrations
    alembic upgrade head
#### Mark database as up to date (if alembic_version table was messed with)
    alembic stamp head
