from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number= db.Column(db.String(9))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('name')
    def validate_name(self, key, name):
        if name=='':
            raise ValueError('Author must have a name')
        if Author.query.filter(Author.name==name).first()==False:
            raise ValueError('Name already exists')
        return name
    
    @validates('phone_number')
    def validates_phone(self, key, phone_number):
        if len(phone_number)<10 or len(phone_number)>10 or isinstance(phone_number, int)==False:
            raise ValueError('Not a valid number')
        return phone_number


    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Must have a title")
        return title

    @validates('content')
    def validate_content(self, key, content):
        if len(content)<250 or len(content)>250:
            raise ValueError('Post content must be 250 characters long')
        return content
    
    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary)>250:
            raise ValueError('Must not be more that 250 characters')
        return summary


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
