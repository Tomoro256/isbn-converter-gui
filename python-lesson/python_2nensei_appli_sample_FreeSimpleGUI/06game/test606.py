def getnextnums(n):
    nextnums = list(range(n+1, min(32, n+4)))
    choicemsg = f"{nextnums} から入力してください。"
    print(choicemsg)

getnextnums(5)
getnextnums(18)
getnextnums(29)