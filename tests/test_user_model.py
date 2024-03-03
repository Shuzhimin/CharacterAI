# 2024/3/2
# zhangzhong

from app.models import User, UserFilter, UserIn, UserOut, UserParams, UserUpdate


def test_user_update():
    user_update = UserUpdate(username="username")
    assert not user_update.is_empty()
    assert UserUpdate().is_empty()

    print(user_update.to_set_clause())
    # 多一点应该没有影响吧
    print(user_update.to_params())


def test_user_filter():
    user_filter = UserFilter(uid=1)
    assert not user_filter.is_empty()
    assert UserFilter().is_empty()

    print(user_filter.to_where_clause())
    print(user_filter.to_params())
