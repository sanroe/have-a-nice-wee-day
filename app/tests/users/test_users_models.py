from app.extensions.database import db
from app.users.models import User

def test_user_update(client):
    # Update user information
    user = User(email='test3@test.test', password='test')
    db.session.add(user)
    db.session.commit()

    user_id = user.id

    user.email = 'test4@test.test'
    user.save()

    updated_user = User.query.filter_by(id=user_id).first()
    assert updated_user.email == 'test4@test.test'