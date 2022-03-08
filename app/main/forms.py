# 存放表单类
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError

from app.models import User, Role
from flask_pagedown.fields import PageDownField


class NameForm(FlaskForm):
    name = StringField('用户名', validators=[DataRequired()])
    submit = SubmitField('提交')

class EditProfileForm(FlaskForm):
    name = StringField('真实姓名', validators=[Length(0, 64)])
    location = StringField('地区',validators=[Length(0, 64)])
    about_me = TextAreaField('关于我')
    submit = SubmitField('提交')




class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               '用户名只能包含数字字母数字点和下划线')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('角色', coerce=int)
    name = StringField('真实姓名', validators=[Length(0, 64)])
    location = StringField('地区', validators=[Length(0, 64)])
    about_me = TextAreaField('关于我')
    submit = SubmitField('提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    #自定义的验证函数，由于有validdate_前缀，所以会自动调用
    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经被注册！')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经被使用！')


class PostForm(FlaskForm):
    body = PageDownField("想发射你的点子？", validators=[DataRequired()])
    submit = SubmitField("提交")


class CommentForm(FlaskForm):
    body = PageDownField("整条评论吧", validators=[DataRequired()])
    submit = SubmitField("提交")