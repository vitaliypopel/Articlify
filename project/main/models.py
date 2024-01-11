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

    def __repr__(self) -> str:
        return f'Topic(\n' \
               f'   id [PK]:    {self.id}\n' \
               f'   topic:      {self.topic}\n' \
               f')'


class TopicSubscription(db.Model):
    __tablename__: str = 'topic_subscriptions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), nullable=False)

    def __init__(self, user_id: int, topic_id: int):
        self.user_id = int(user_id)
        self.topic_id = int(topic_id)

    def __repr__(self) -> str:
        return f'TopicSubscription(\n' \
               f'   id [PK]:        {self.id}\n' \
               f'   user_id [FK]:   {self.user_id}\n' \
               f'   topic_id [FK]:  {self.topic_id}\n' \
               f')'


class UserSubscription(db.Model):
    __tablename__: str = 'user_subscriptions'

    id = db.Column(db.Integer, primary_key=True)
    subscribed_at = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, user_id: int, author_id: int):
        self.user_id = int(user_id)
        self.author_id = int(author_id)
        self.subscribed_at = datetime.utcnow()

    def __repr__(self) -> str:
        return f'UserSubscription(\n' \
               f'   id [PK]:        {self.id}\n' \
               f'   subscribed_at:  {self.subscribed_at}\n' \
               f'   user_id [FK]:   {self.user_id}\n' \
               f'   author_id [FK]: {self.author_id}\n' \
               f')'


class UserSubscriptionRequest(db.Model):
    __tablename__: str = 'user_subscription_requests'

    id = db.Column(db.Integer, primary_key=True)
    sent_at = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, user_id: int, author_id: int):
        self.user_id = int(user_id)
        self.author_id = int(author_id)
        self.sent_at = datetime.utcnow()

    def __repr__(self) -> str:
        return f'UserSubscriptionRequest(\n' \
               f'   id [PK]:        {self.id}\n' \
               f'   sent_at:        {self.sent_at}\n' \
               f'   user_id [FK]:   {self.user_id}\n' \
               f'   author_id [FK]: {self.author_id}\n' \
               f')'


class Article(db.Model):
    __tablename__: str = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(80), nullable=False)
    public = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, default=None, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, title: str, link: str, public: bool, user_id: int):
        self.title = title
        self.link = link
        self.public = bool(public)
        self.user_id = int(user_id)
        self.created_at = datetime.utcnow()

    def __repr__(self) -> str:
        return f'Article(\n' \
               f'   id [PK]:        {self.id}\n' \
               f'   title:          {self.title}\n' \
               f'   link:           {self.link}\n' \
               f'   public:         {self.public}\n' \
               f'   created_at:     {self.created_at}\n' \
               f'   updated_at:     {self.updated_at}\n' \
               f'   user_id [FK]:   {self.user_id}\n' \
               f')'


class ArticleView(db.Model):
    __tablename__: str = 'article_views'

    id = db.Column(db.Integer, primary_key=True)
    viewed_at = db.Column(db.DateTime, nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, article_id: int, user_id: int):
        self.article_id = int(article_id)
        self.user_id = int(user_id)
        self.viewed_at = datetime.utcnow()

    def __repr__(self) -> str:
        return f'ArticleView(\n' \
               f'   id [PK]:            {self.id}\n' \
               f'   viewed_at:          {self.viewed_at}\n' \
               f'   article_id [FK]:    {self.article_id}\n' \
               f'   user_id [FK]:       {self.user_id}\n' \
               f')'


class ArticleLike(db.Model):
    __tablename__: str = 'article_likes'

    id = db.Column(db.Integer, primary_key=True)
    liked_at = db.Column(db.DateTime, nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, article_id: int, user_id: int):
        self.article_id = int(article_id)
        self.user_id = int(user_id)
        self.liked_at = datetime.utcnow()

    def __repr__(self) -> str:
        return f'ArticleLike(\n' \
               f'   id [PK]:            {self.id}\n' \
               f'   liked_at:           {self.liked_at}\n' \
               f'   article_id [FK]:    {self.article_id}\n' \
               f'   user_id [FK]:       {self.user_id}\n' \
               f')'


class ArticleComment(db.Model):
    __tablename__: str = 'article_comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(300), nullable=False)
    commented_at = db.Column(db.DateTime, nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, comment: str, article_id: int, user_id: int):
        self.comment = comment
        self.article_id = int(article_id)
        self.user_id = int(user_id)
        self.commented_at = datetime.utcnow()

    def __repr__(self) -> str:
        return f'ArticleComment(\n' \
               f'   id [PK]:            {self.id}\n' \
               f'   comment:            {self.comment}\n' \
               f'   commented_at:       {self.commented_at}\n' \
               f'   article_id [FK]:    {self.article_id}\n' \
               f'   user_id [FK]:       {self.user_id}\n' \
               f')'


class ArticleTopic(db.Model):
    __tablename__: str = 'article_topics'

    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), nullable=False)

    def __init__(self, article_id: int, topic_id: int):
        self.article_id = int(article_id)
        self.topic_id = int(topic_id)

    def __repr__(self) -> str:
        return f'ArticleTopic(\n' \
               f'   id [PK]:            {self.id}\n' \
               f'   article_id [FK]:    {self.article_id}\n' \
               f'   topic_id [FK]:      {self.topic_id}\n' \
               f')'
