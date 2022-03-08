import os

COV = None
if os.environ.get('FLASK_COVERAGE'):
    #此函数用于启动覆盖检测检查，branch用于开启分支检查，确保每个分支都得到执行，include表示代码测试范围
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

import sys
from flask_migrate import Migrate
from app import create_app, db
from app.models import User, Role, Post, Comment, Permission
#from flask_bootstrap import WebCDN,ConditionalCDN,BOOTSTRAP_VERSION,JQUERY_VERSION,HTML5SHIV_VERSION,RESPONDJS_VERSION
import click


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)




# 使用国内源的bootstrap
# def change_cdn_domestic(tar_app):
#     static = tar_app.extensions['bootstrap']['cdns']['static']
#     local = tar_app.extensions['bootstrap']['cdns']['local']
#
#     def change_one(tar_lib, tar_ver, fallback):
#         tar_js = ConditionalCDN('BOOTSTRAP_SERVE_LOCAL', fallback,
#                                 WebCDN('//cdn.bootcss.com/' + tar_lib + '/' + tar_ver + '/'))
#         tar_app.extensions['bootstrap']['cdns'][tar_lib] = tar_js
#
#     libs = {'jquery': {'ver': JQUERY_VERSION, 'fallback': local},
#             'bootstrap': {'ver': BOOTSTRAP_VERSION, 'fallback': local},
#             'html5shiv': {'ver': HTML5SHIV_VERSION, 'fallback': static},
#             'respond.js': {'ver': RESPONDJS_VERSION, 'fallback': static}}
#     for lib, par in libs.items():
#         change_one(lib, par['ver'], par['fallback'])
#
#
# change_cdn_domestic(app)




@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Post=Post, Comment=Comment, Permission=Permission)


@app.cli.command("test")
@click.option('--coverage/--no-coverage', default=False,
              help='Run tests under code coverage.')
@click.argument('test_names', nargs=-1)
def test(coverage, test_names):
    """Run the unit tests."""
    #此时开启代码检测时机已晚， 需要重新启动脚本以支持代码测试
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import subprocess
        os.environ['FLASK_COVERAGE'] = '1'
        sys.exit(subprocess.call(sys.argv))

    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()

@app.cli.command()
@click.option('--length', default=25,
              help='Number of functions to include in the profiler report.')
@click.option('--profile-dir', default=None,
              help='Directory where profiler data files are saved.')
def profile(length, profile_dir):
    """Start the application under the code profiler."""
    from werkzeug.middleware.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    app.run()



@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    from flask_migrate import upgrade
    db.create_all()
    upgrade()

    # create or update user roles
    Role.insert_roles()

    # ensure all users are following themselves
    User.add_self_follows()




