from project import db, UserMixin, datetime


class User(db.Model, UserMixin):
    __tablename__: str = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    profile_picture_path = db.Column(db.String(100), nullable=False, default='photos/profile_pictures/default_pfp.svg')
    public_profile = db.Column(db.Boolean, nullable=False, default=True)
    email_status = db.Column(db.Boolean, nullable=False, default=False)
    registration = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self) -> str:
        return f'User(\n' \
               f'   id [PK]:                {self.id}\n' \
               f'   username:               {self.username}\n' \
               f'   password:               {self.password}\n' \
               f'   email:                  {self.email}\n' \
               f'   profile_picture_path:   {self.profile_picture_path}\n' \
               f'   public_profile:         {self.public_profile}\n' \
               f'   email_status:           {self.email_status}\n' \
               f'   registration:           {self.registration}\n' \
               f')'

