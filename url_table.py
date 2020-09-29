def init_url():
    from app import api

    import Session.app
    api.add_resource(Session.app.Session, '/api/session')

    import Config.app
    api.add_resource(Config.app.YZM, '/api/config/captcha')
    api.add_resource(Config.app.Token, '/api/config/csrf')

    import User.app
    api.add_resource(User.app.User, '/api/user', '/api/user/<int:uid>')
    api.add_resource(User.app.Avatar, '/api/avatar')
    api.add_resource(User.app.PWD, '/api/pwd')

    import Info.app
    api.add_resource(Info.app.AnnList, '/api/info/ann')
    api.add_resource(Info.app.Ann, '/api/info/ann/<int:aid>')

    import Tag.app
    api.add_resource(Tag.app.Tag, '/api/tag/<int:level>/<int:father>', '/api/tag/<int:level>')
    api.add_resource(Tag.app.TagChooseQu, '/api/choose/tag/<int:tid>/<int:level>')

    import Question.app
    api.add_resource(Question.app.Qu, '/api/qu/<int:qid>')
    api.add_resource(Question.app.Judge, '/api/judge/<int:jid>')
