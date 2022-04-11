from django.apps import AppConfig
from gensim.models import word2vec

class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"


class W2V(AppConfig):
    model_filename = 'accounts/model/kor_word2vec.model'

    model = word2vec.Word2Vec.load(model_filename)