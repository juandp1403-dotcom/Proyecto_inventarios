from app import create_app
app = create_app()
with app.app_context():
    for rule in sorted(app.url_map.iter_rules(), key=lambda r:(r.rule, r.endpoint)):
        print(f'{rule.rule:40} {sorted(rule.methods)} {rule.endpoint}')
