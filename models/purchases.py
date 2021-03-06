from app import db
from models.resellers import Reseller


class Purchase(db.Model):
    __tablename__ = 'purchases'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(80))
    value = db.Column(db.Float())
    date = db.Column(db.DateTime())
    status = db.Column(db.String(20), default='Em validação')

    reseller_cpf = db.Column(db.String(11), db.ForeignKey('resellers.cpf'))
    reseller = db.relationship('Reseller')

    def __init__(self, **kwargs):
        super(Purchase, self).__init__(**kwargs)

    @classmethod
    def find_by_cpf(cls, cpf):
        return cls.query.filter_by(cpf=cpf).first()

    @classmethod
    def find_by_reseller(cls, id):
        cpf = Reseller.find_by_id(id).cpf
        return cls.query.filter_by(reseller_cpf=cpf)

    def to_json(self):
        if self.value <= 1000:
            cashback_percent = '10%'
            cashback = self.value * 0.1
        elif self.value <= 1500:
            cashback_percent = '15%'
            cashback = self.value * 0.15
        else:
            cashback_percent = '20%'
            cashback = self.value * 0.2

        purchase = {
            'code': self.code,
            'value': self.value,
            'date': self.date,
            '% cashback': cashback_percent,
            'cashback': cashback,
            'status': self.status
        }
        return purchase

    @staticmethod
    def from_json(json_post):
        code = json_post.get('code')
        value = json_post.get('value')
        date = json_post.get('date')
        cpf = json_post.get('reseller_cpf')

        reseller_cpf = cpf.replace('-', '').replace('.', '')

        if reseller_cpf == '15350946056':
            status = 'Aprovado'
        else:
            status = 'Em validação'

        purchase = Purchase(
            code=code,
            value=value,
            date=date,
            reseller_cpf=reseller_cpf,
            status=status
        )
        return purchase

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
