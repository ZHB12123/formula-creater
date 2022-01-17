import random
from formula_tools import RPN2IN, IN2RPN, evalRPN, Stack


def create_RPN(num, min_number, max_number):
    symbols = "+-*/"
    str_ = str(random.randint(min_number, max_number))
    str_list = [str_]
    S = Stack()
    S.push(str_)

    symbols_num = 0
    numbers_num = 0

    for i in range(num * 2):
        if S.size() <= 1:
            str_ = str(random.randint(min_number, max_number))
            str_list.append(str_)
            S.push(str_)
            numbers_num += 1
            continue
        if S.size() > 1:
            push_flag = random.randint(0, 1)
            if numbers_num >= num:
                push_flag = 1
            if symbols_num >= num:
                push_flag = 0
            if push_flag == 0:
                str_ = str(random.randint(min_number, max_number))
                str_list.append(str_)
                S.push(str_)
                numbers_num += 1
            if push_flag == 1:
                str_ = symbols[random.randint(0, 3)]
                str_list.append(str_)
                S.pop()
                symbols_num += 1
                continue
    return str_list


def check_brackets(infix_notation):
    """
    判断括号是否合法
    :param infix_notation:
    :return:
    """
    S = Stack()
    for c in infix_notation:
        if c == "(":
            S.push(c)
        if c == ")":
            if S.size() == 0:
                return False
            if S.top() == "(":
                S.pop()
            else:
                return False
    return True


def remove_brackets(reverse_polish_notation, infix_notation):
    """

    :param reverse_polish_notation:
    :param infix_notation:
    :return:
    """
    p1 = 0
    p2 = len(infix_notation) - 1
    while p1 < p2:
        if infix_notation[p1] == "(" and infix_notation[p2] == ")":
            IN = infix_notation.copy()
            IN[p1] = ""
            IN[p2] = ""
            for i in range(IN.count("")):
                IN.remove("")
            if not check_brackets(IN):
                break
            if IN2RPN(IN) == reverse_polish_notation:
                infix_notation[p1] = ""
                infix_notation[p2] = ""
            else:
                break
            p1 += 1
            p2 -= 1
        if infix_notation[p1] == "(" and infix_notation[p2] != ")":
            p2 -= 1
        if infix_notation[p1] != "(" and infix_notation[p2] == ")":
            p1 += 1
        if infix_notation[p1] != "(" and infix_notation[p2] != ")":
            p1 += 1
    for i in range(infix_notation.count("")):
        infix_notation.remove("")
    return infix_notation


def create_basic_formula(count, symbols_count, min_number, max_number):
    """
    生成算式
    :param count: 生成数量
    :param symbols_count:每个算式符号数量
    :param min_number: 算式中最小数
    :param max_number: 算式中最大数
    :return:
    """
    n = 0
    result = []
    while n < count:
        str_list = create_RPN(symbols_count, min_number, max_number)
        try:
            answer = evalRPN(str_list)
            infix_notation_list = RPN2IN(str_list)
            final_infix_notation_list = remove_brackets(str_list, infix_notation_list)
            result.append({"infix_notation": final_infix_notation_list, "answer": answer})
            n += 1
        except ZeroDivisionError:
            pass
    return result


a = create_basic_formula(100000, 3, 0, 100)
for i in a:
    # print(i)
    # print("".join(i["infix_notation"]))
    if (eval("".join(i["infix_notation"])) != i["answer"]):
        print("计算结果不一致")
        raise Exception("计算结果不一致")
