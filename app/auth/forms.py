from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo

from app.models import User


class LoginForm(FlaskForm):
    email = StringField('电子邮件', validators=[DataRequired(), Length(1, 64), Email()])

    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


class RegistrationForm(FlaskForm):
    email = StringField('电子邮件', validators=[DataRequired(), Length(1,64), Email()])

    username = StringField('用户名', validators=[DataRequired(),Length(1,64),
                                              Regexp('^[A-Za-z][A-Za-z0-9._]*$',0, '用户名只能包含数字字母数字点和下划线')])
    password = PasswordField('密码', validators=[DataRequired(), EqualTo('password2','两次密码不一致')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])

    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮件已经注册!')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经被使用!')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('旧密码', validators=[DataRequired()])
    password = PasswordField('新密码', validators=[DataRequired(),
                                                EqualTo('password2', message='两次密码必须一致')])
    password2 = PasswordField('确认新密码', validators=[DataRequired()])

    submit = SubmitField('更新密码')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('电子邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    submit = SubmitField('重置密码')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('新密码', validators=[DataRequired(),
                                                EqualTo('password2', message='两次密码不一致!')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('重置密码')
