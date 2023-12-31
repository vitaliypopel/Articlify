from project import db, datetime


class Feedback(db.Model):
    __tablename__: str = 'feedbacks'

    id = db.Column(db.Integer, primary_key=True)
    sender_email = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    sent_at = db.Column(db.DateTime, nullable=False)
    body = db.Column(db.String(1000), nullable=True)

    def __init__(self, sender_email: str, category: str, body: str):
        self.sender_email = sender_email.lower()
        self.category = category
        self.body = body
        self.sent_at = datetime.utcnow()

    def __repr__(self) -> str:
        return f'Feedback(\n' \
               f'   id [PK]:        {self.id}\n' \
               f'   sender_email:   {self.sender_email}\n' \
               f'   category:       {self.category}\n' \
               f'   sent_at:        {self.sent_at}\n' \
               f'   body:           {self.body}\n' \
               f')'


class Topic(db.Model):
    __tablename__: str = 'topics'

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(100), nullable=False)

    def __init__(self, topic: str):
        self.topic = topic

    def __repr__(self):
        return f'Topic(\n' \
               f'   id [PK]:    {self.id}\n' \
               f'   topic:      {self.topic}\n' \
               f')'
