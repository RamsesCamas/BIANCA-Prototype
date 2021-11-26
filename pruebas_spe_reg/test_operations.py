import operator

operations = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}

def eval_binary_expr(op1, oper, op2):
    op1, op2 = int(op1), int(op2)
    return operations[oper](op1, op2)

def sumNum(num1,*args):
    res = num1
    for arg in args:
        res = res + arg
    return res

ops = {'+': sumNum}


if __name__ == '__main__':
    #print(eval_binary_expr(*("10 + 5".split())))
    print(ops['+'](1,2,20))
    print(eval('10 + 5 + 20'))
    #print(sumNum(10,5,20))