from app import create_app
app = create_app()
with app.test_request_context():
    for rule in sorted(app.url_map.iter_rules(), key=lambda r: r.rule):
        print(rule.endpoint, rule.rule, sorted(rule.methods))
