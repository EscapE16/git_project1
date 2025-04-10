from data.jobs import jobs
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_name = input().strip()
    global_init(db_name)
    session = create_session()

    colonists = session.query(User).filter(User.address.like('module_1%')).all()
    for colonist in colonists:
        print(colonist)


if __name__ == '__main__':
    main()