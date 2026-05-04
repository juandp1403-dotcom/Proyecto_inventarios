from app import create_app
app = create_app()
with app.test_request_context():
    print('Routes:')
    for rule in app.url_map.iter_rules():
        print(rule.endpoint, rule.rule, sorted(rule.methods))
