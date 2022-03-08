| 资源（客户端支持的功能）   | 方     法 |                    说   明                     |
| :------------------------- | :-------: | :--------------------------------------------: |
| /users/<int: id>           |    GET    |               获得一个用户的信息               |
| /users/<int: id>/posts/    |    GET    |        获得一个用户发表的博客的相关信息        |
| /users/<int: id>/timeline/ |    GET    |       获得一个用户关注的所有人的博客信息       |
| /posts/                    | GET, POST |       获得所有博客信息，或发表自己的博客       |
| /posts/<int: id>           |  GET,PUT  |         获得指定id的博客或者修改该博客         |
| /posts/<int: id>/comments/ | GET,POST  | 获得指定id的博客的所有评论或者对此发表一个评论 |
| /comments/                 |    GET    |                  获得所有评论                  |
| /comments/<int: id>        |    GET    |                获得指定id的评论                |

### ps:如果想增加功能，请到对应的_name_.py下增加对应的视图函数。 ###

