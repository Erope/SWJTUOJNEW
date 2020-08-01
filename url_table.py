def init_url():
    from app import api

    import Session.app
    api.add_resource(Session.app.Session, '/api/session')

    import Config.app
    api.add_resource(Config.app.YZM, '/api/config/captcha')
    api.add_resource(Config.app.Token, '/api/config/csrf')

    import User.app
    api.add_resource(User.app.User, '/api/user', '/api/user/<int:uid>')
