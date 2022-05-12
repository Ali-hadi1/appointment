from appointment import db

class Notification(db.Model):
    __tablename__='Notification'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.String(200), nullable=False)
    viewed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Notification('{self.id}', '{self.user_id}', '{self.message}'," \
               f"'{self.viewed}')"

    def __init__(self, user_id, message):
        self.user_id = user_id
        self.message = message
        db.session.add(self)
        db.session.commit()

    def viewed(self):
        self.viewed = True
        db.session.commit()

