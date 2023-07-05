from pony.orm import *
from datetime import datetime, timedelta
import pandas as pd
import time, random


# region start
def func_exec_time(f):
    def inner(*arg, **kwarg):
        s_time = time.time()
        res = f(*arg, **kwarg)
        e_time = time.time()
        print(
            f'::Monitor:: "{f.__name__}" execute second(s)：{round(e_time - s_time, 4)}'
        )
        return res

    return inner


def float2percentage(f: float, decimalplace=2) -> str:
    t = str(f * 100)
    if '.' not in t:
        return t + "%"

    t = t.rstrip('0')
    position = t.find('.')
    if len(t[position + 1:]) == 0:
        return t.rstrip('.') + "%"
    elif len(t[position + 1:]) <= decimalplace:
        return t.rstrip('0') + "%"
    else:
        return str(round(f * 100, decimalplace)) + "%"


def get_rate_of_chage(a: float, b: float):
    if b == 0:
        return {"ret": "fail", "code": -1, 'msg': "对比值不接受0"}
    return float2percentage((a - b) / b)


# endregion

db = Database()
# db.bind(provider='postgres', user='postgres', password='111111', host='localhost', port=5432, database='mars')
db.bind(provider='sqlite', filename=':memory:', create_db=True)

# order_file_path = r"http://192.168.1.14/order.xlsx"
# user_file_path = r"http://192.168.1.14/user.xlsx"
order_file_path = r"C:\Users\liang\Desktop\Repo\order.xlsx"
user_file_path = r"C:\Users\liang\Desktop\Repo\user.xlsx"


class User(db.Entity):
    code = Optional(str)
    name = Optional(str)
    create_time = Optional(datetime)

    # relationship
    order = Set("Order")


class Order(db.Entity):
    user = Optional(User, reverse="order")

    order_num = Optional(str)
    account_name = Optional(str)
    school = Optional(str)
    amount = Optional(float)
    deal_time = Optional(datetime)


@db_session
def save_user(args: list):
    # paras: list of dict like {order_num, user_id, account_name, school, amount, deal_time}
    if len(args) <= 0 or len(args) > 3000:
        return {"ret": "fail", "code": -1, 'msg': "每次批量保存数据数量限定1~3000"}

    items = 0
    for i in range(len(args)):
        # if exist
        # pass
        try:
            # if select(o for o in Order if o.order_num == args[i]["order_num"]).exists():
            #     continue

            user = User()
            user.code = str(args[i]["user_id"])
            user.name = str(args[i]["name"])
            user.create_time = args[i]["create_time"]

            items += 1
            # orders.append(order)
        except Exception as e:
            print(f"{__name__}Warning:", e)

    return {
        "ret": "sucess",
        "code": 200,
        'msg': f"收到{len(args)}条数据，保存{items}条，{len(args) - items}条无法解析或已存在"
    }


@db_session
def save_orders(args: list):
    # paras: list of dict like {order_num, user_id, account_name, school, amount, deal_time}
    if len(args) <= 0 or len(args) > 3000:
        return {"ret": "fail", "code": -1, 'msg': "每次批量保存数据数量限定1~3000"}

    orders = []
    for i in range(len(args)):
        # if exist
        # pass
        try:
            # if select(o for o in Order if o.order_num == args[i]["order_num"]).exists():
            #     continue

            order = Order()
            order.order_num = args[i]["order_num"]
            # order.user = select(u for u in User if u.code == str(args[i]["user_id"])).first()
            order.user = User.get(code=str(args[i]["user_id"]))
            order.account_name = str(args[i]["account_name"])
            order.school = args[i]["school"]
            order.amount = args[i]["amount"]
            order.deal_time = args[i]["deal_time"]

            orders.append(order)
        except Exception as e:
            print("Warning:", e)

    return {
        "ret":
        "sucess",
        "code":
        200,
        'msg':
        f"收到{len(args)}条数据，保存{len(orders)}条，{len(args) - len(orders)}条无法解析或已存在"
    }


@func_exec_time
def save2():
    df = pd.read_excel(user_file_path)
    # print(df.head(5))
    # data = {
    #     "order_num":None,
    #     "user_id": None,
    #     "account_name": None,
    #     "school": None,
    #     "amount": None,
    #     "deal_time":None,
    # }
    data_list = []
    for i in df.index:
        data = {
            "create_time": df.loc[i, "账号创建时间"],
            "user_id": df.loc[i, "用户id"],
            "name": df.loc[i, "用户名"],
        }
        data_list.append(data)

    # print(data_list[:2])
    print(save_user(data_list))


@func_exec_time
def save():
    df = pd.read_excel(order_file_path)
    # print(df.head(5))
    # data = {
    #     "order_num":None,
    #     "user_id": None,
    #     "account_name": None,
    #     "school": None,
    #     "amount": None,
    #     "deal_time":None,
    # }
    data_list = []
    for i in df.index:
        data = {
            "order_num": df.loc[i, "订单号"],
            "user_id": df.loc[i, "用户id"],
            "account_name": df.loc[i, "排课账号"],
            "school": df.loc[i, "学校名称"],
            "amount": df.loc[i, "金额"],
            "deal_time": df.loc[i, "充值时间"],
        }
        data_list.append(data)

    print(save_orders(data_list))


@func_exec_time
@db_session
def static():
    # count = select(i for i in Order if i.amount < 300).count()
    # total_amount = sum(i.amount for i in Order if i.amount > 100)
    # all = select(i for i in Order)
    #
    # user_has_2 = select(u for u in User if len(u.order) >= 2)
    # for x in user_has_2[:2]:
    #     print(x.order.order_num,x.order.amount,x.order.deal_time)
    #
    # print(count, total_amount, float2percentage(len(user_has_2)/len(all)))

    # 每月 付费用户，付费金额，复购用户，累计复购率
    scope = timedelta(weeks=1)
    offset = timedelta(days=1)
    start_date = datetime(year=2021,
                          month=12,
                          day=17,
                          hour=0,
                          minute=0,
                          second=0,
                          microsecond=0)

    # dataframe
    columns = ['period', 'Paid User', 'Amount']
    data = []
    # gen data
    while True:
        end_date = start_date + scope

        period = f'{str(start_date.year)[-2:]}/{start_date.month}/{start_date.day}~{str(end_date.year)[-2:]}/{end_date.month}/{end_date.day} '
        ord = select(o for o in Order
                     if between(o.deal_time, start_date, end_date))
        amount = select(o.amount for o in ord).sum()
        # pu = select(o.user for o in ord).distinct()
        # ru = select(o.user for o in ord if len(o.user.order) >= 2)

        # for x in ru:
        #     print(x)
        #
        # print(ord.count(),
        #       amount,
        #       pu.count(),
        #       ru.count()
        #       )
        d = (period, len(ord), amount)
        data.append(d)

        # break
        # print(end_date,datetime.now())
        if end_date > datetime.now():
            break

        start_date = end_date + offset

    df = pd.DataFrame(data=data, columns=columns)
    df.to_csv(r'C:\Users\liang\Desktop\Repo\{name}.csv'.format(
        name=random.randint(1, 10000)))
    print(df)
    rr = float2percentage(
        select(u for u in User if len(u.order) >= 2).count() /
        select(u for u in User).count())
    print(rr)


@func_exec_time
@db_session
def compare():
    start_date = datetime(year=2022,
                          month=4,
                          day=15,
                          hour=0,
                          minute=0,
                          second=0,
                          microsecond=0)
    end_date = datetime(year=2022,
                        month=7,
                        day=1,
                        hour=0,
                        minute=0,
                        second=0,
                        microsecond=0)

    o_c = count(o for o in Order if between(o.deal_time, start_date, end_date))
    o_a = sum(o.amount for o in Order
              if between(o.deal_time, start_date, end_date))

    print(o_c, o_a)

    start_date = datetime(year=2023,
                          month=4,
                          day=15,
                          hour=0,
                          minute=0,
                          second=0,
                          microsecond=0)
    end_date = datetime(year=2023,
                        month=7,
                        day=1,
                        hour=0,
                        minute=0,
                        second=0,
                        microsecond=0)

    o_c = count(o for o in Order if between(o.deal_time, start_date, end_date))
    o_a = sum(o.amount for o in Order
              if between(o.deal_time, start_date, end_date))

    print(o_c, o_a)

    print(count(u for u in User))


if __name__ == '__main__':
    db.generate_mapping(create_tables=True)
    # save2()
    # save()
    # static()
    # # for x in range(10):
    #     time.sleep(1)
    #     static()
    compare()
