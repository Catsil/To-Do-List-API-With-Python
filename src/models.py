from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(250), unique=False, nullable=False)
    done = db.Column(db.Boolean, unique=False, nullable=False)
    
    def __repr__(self):
        return f'Task is :{self.item}, done:{self.done}, id:{self.id}'

    def to_dict(self):
        return {
            "id": self.id,
            "item": self.item,
            "done": self.done
            # do not serialize the password, its a security breach
        }

    @classmethod
    def get_by_id(cls,id_task):
        task= cls.query.filter_by(id=id_task).one_or_none()
        return task
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def get_all(cls):
        tasks= cls.query.all()
        return tasks

    def update(self, item):
        self.item=item
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self
@classmethod
    def get_by_item(cls,item):
        account = cls.query.filter_by(item = item).one_or_none()
        return account