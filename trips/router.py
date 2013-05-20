class TripRouter(object):
    def db_for_read(self, model, **hints):
        if type(model).__name__ == "Track":
            return 'mp3s'
        return 'default'

    def db_for_write(self, model, **hints):
        if type(model).__name__ == "Track":
            return 'mp3s'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_syncdb(self, db, model):
        return True