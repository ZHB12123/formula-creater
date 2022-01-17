class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return True if len(self.items) == 0 else False

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def top(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)

    def pop_front(self):
        return self.items.pop(0)


class Tree(object):
    def __init__(self, data=None, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

    def preorder(self):
        """
        前序遍历
        :return:
        """
        if self.data is not None:
            print(self.data, end=" ")
        if self.left is not None:
            self.left.preorder()
        if self.right is not None:
            self.right.preorder()

    def inorder(self, result):
        """
        中序遍历
        :param result:
        :return:
        """
        if self.left is not None:
            result.append("(")
            self.left.inorder(result)
        if self.data is not None:
            result.append(self.data)
        if self.right is not None:
            self.right.inorder(result)
            result.append(")")

    def postorder(self):
        """
        后序遍历
        :return:
        """
        if self.left is not None:
            self.left.postorder()
        if self.right is not None:
            self.right.postorder()
        if self.data is not None:
            print(self.data, end=" ")

    def levelorder(self):
        """
        层序遍历
        :return:
        """

        def LChild_Of_Node(node):
            return node.left if node.left is not None else None

        def RChild_Of_Node(node):
            return node.right if node.right is not None else None

        level_order = []
        if self.data is not None:
            level_order.append([self])

        height = self.height()
        if height >= 1:
            for _ in range(2, height + 1):
                level = []
                for node in level_order[-1]:
                    if LChild_Of_Node(node):
                        level.append(LChild_Of_Node(node))
                    if RChild_Of_Node(node):
                        level.append(RChild_Of_Node(node))
                if level:
                    level_order.append(level)
            for i in range(0, height):
                for index in range(len(level_order[i])):
                    level_order[i][index] = level_order[i][index].data

        return level_order

    def height(self):
        """
        二叉树高度
        :return:
        """
        if self.data is None:
            return 0
        elif self.left is None and self.right is None:
            return 1
        elif self.left is None and self.right is not None:
            return 1 + self.right.height()
        elif self.left is not None and self.right is None:
            return 1 + self.left.height()
        else:
            return 1 + max(self.left.height(), self.right.height())

    def leaves(self):
        """
        二叉树的叶子节点
        :return:
        """
        if self.data is None:
            return None

        elif self.left is None and self.right is None:
            print(self.data, end=" ")
        elif self.left is None and self.right is not None:
            self.right.leaves()
        elif self.right is None and self.left is not None:
            self.left.leaves()
        else:
            self.left.leaves()
            self.right.leaves()


def RPN2IN(str_list):
    """
    后缀表达式转中缀表达式
    :param str_list:后缀表达式列表
    :return:中缀表达式列表
    """
    characters = "+-*/"
    Len = len(str_list)

    tp = Tree()
    t1 = Tree()
    t2 = Tree()

    S = Stack()

    for i in range(Len):
        t = Tree()
        t.data = str_list[i]
        if str_list[i] not in characters:
            t.left = None
            t.right = None
            S.push(t)
        else:
            t1 = S.top()
            S.pop()
            t2 = S.top()
            S.pop()
            t.left = t2
            t.right = t1
            S.push(t)

    tp = S.top()
    S.pop()
    result = []
    tp.inorder(result)
    return result


def IsSym(ch):
    hh = ["+", "-", "*", "/"]
    for i in range(len(hh)):
        if ch == hh[i]:
            return True
    return False


def Predence(sg_1, sg_2):
    """
    运算符优先级判断
    :param sg_1:
    :param sg_2:
    :return:
    """
    if sg_1 == "(":
        return -1
    if sg_1 == "+" or sg_1 == "-":
        if sg_2 == "*" or sg_2 == "/":
            return -1
        else:
            return 0
    if sg_1 == "*" or sg_1 == "/":
        if sg_2 == '+' or sg_2 == "-":
            return 1
        else:
            return 0


def IN2RPN(inFix):
    """
    中缀表达式转后缀表达式
    :param inFix: 中缀表达式列表
    :return: 后缀表达式列表
    """
    mm = []
    postFix = []
    for i in range(len(inFix)):
        fg = inFix[i]
        if fg == "(":
            mm.append(fg)
        elif fg == ")":
            while mm[-1] != "(":
                postFix.append(mm.pop())
            mm.pop()
        else:
            if IsSym(fg) == False:
                postFix.append(fg)
            else:
                while len(mm) != 0 and Predence(mm[-1], fg) >= 0:
                    postFix.append(mm.pop())
                mm.append(fg)

    while len(mm) != 0:
        postFix.append(mm.pop())

    return postFix


def evalRPN(tokens):
    """
    计算后缀表达式的结果
    :param tokens:
    :return:
    """
    f1 = lambda a, b: a + b
    f2 = lambda a, b: a - b
    f3 = lambda a, b: a * b
    f4 = lambda a, b: a / b

    maps = {"+": f1, "-": f2, "*": f3, "/": f4}
    stack = []
    for i in tokens:
        if i in maps:
            a = stack.pop()
            b = stack.pop()
            stack.append(maps[i](b, a))
        else:
            i = float(i)
            stack.append(i)

    return stack[-1]



