from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)


# модель для дат и координат, которые вводит пользователь
class Search_params(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dt_start = db.Column(db.DateTime, nullable=False)
    dt_finish = db.Column(db.DateTime, nullable=False)
    latitude = db.Column(db.String, nullable=False)
    longitude = db.Column(db.String, nullable=False)

    def __repr__(self):
        return "<search_params {} - {}, {} - {}>".format(self.dt_start,
                                                         self.dt_finish,
                                                         self.latitude,
                                                         self.longitude)


# модель записи в БД для новостей
class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    link = db.Column(db.String)
    date_and_time = db.Column(db.DateTime, index=True)
    text = db.Column(db.String)
    address = db.Column(db.String)
    street = db.Column(db.String)
    lat = db.Column(db.Numeric)
    lon = db.Column(db.Numeric)

    def __repr__(self):
        return "<news record {}>".format(self.id)
