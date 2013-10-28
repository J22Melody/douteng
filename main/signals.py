from django.dispatch import Signal

question_followed = Signal(providing_args=["follower","followed"])
user_followed = Signal(providing_args=["follower","followed"])