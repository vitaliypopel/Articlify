from project import db, UserMixin, datetime, timedelta, token_urlsafe


class User(db.Model, UserMixin):
    __tablename__: str = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    bio = db.Column(db.String(1000), nullable=False, default='')
    profile_picture = db.Column(db.String(100), nullable=False, default='default_pfp.png')
    profile_status = db.Column(db.Boolean, nullable=False, default=True)
    email_status = db.Column(db.Boolean, nullable=False, default=False)
    registration = db.Column(db.DateTime, nullable=False)

    def __init__(self, username: str, password: str, email: str):
        self.username = username.lower()
        self.password = password
        self.email = email.lower()
        self.registration = datetime.utcnow()

    def __repr__(self) -> str:
        return f'User(\n' \
               f'   id [PK]:                {self.id}\n' \
               f'   username:               {self.username}\n' \
               f'   password:               {self.password}\n' \
               f'   email:                  {self.email}\n' \
               f'   bio:                    {self.bio}\n' \
               f'   profile_picture:        {self.profile_picture}\n' \
               f'   profile_status:         {self.profile_status}\n' \
               f'   email_status:           {self.email_status}\n' \
               f'   registration:           {self.registration}\n' \
               f')'


class EmailConfirmation(db.Model):
    __tablename__: str = 'email_confirmations'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(100), nullable=False, unique=True)
    expiration_time = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, user_id: int):
        self.user_id = int(user_id)
        self.token = token_urlsafe(30)
        self.expiration_time = datetime.utcnow() + timedelta(hours=24)

    def __repr__(self) -> str:
        return f'EmailConfirmation(\n' \
               f'   id [PK]:            {self.id}\n' \
               f'   token:              {self.token}\n' \
               f'   expiration_time:    {self.expiration_time}\n' \
               f'   user_id [FK]:       {self.user_id}\n' \
               f')'


class ResetPassword(db.Model):
    __tablename__: str = 'reset_passwords'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(100), nullable=False, unique=True)
    expiration_time = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, user_id: int):
        self.user_id = int(user_id)
        self.token = token_urlsafe(30)
        self.expiration_time = datetime.utcnow() + timedelta(minutes=30)

    def __repr__(self) -> str:
        return f'ResetPassword(\n' \
               f'   id [PK]:            {self.id}\n' \
               f'   token:              {self.token}\n' \
               f'   expiration_time:    {self.expiration_time}\n' \
               f'   user_id [FK]:       {self.user_id}\n' \
               f')'
