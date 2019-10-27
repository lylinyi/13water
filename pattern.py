# 普通牌型
def takeSecond(elem):
    return elem[1]


class Card:
    # [0,0,1,2...]从2开始

    # card参数格式[(1,1),(2,3)]
    def __init__(self, card):
        self.card = card
        self.card.sort(key=takeSecond)
        self.cnt_num = [0 for i in range(0, 15)]
        self.cnt_color = [0 for i in range(0, 4)]
        for c in card:
            self.cnt_num[c[1]] += 1
            self.cnt_color[c[0]] += 1
        if len(card)>5:
            print("-------------牌型--------------------")
            print(card)
            print(self.cnt_num)
            print(self.cnt_color)
            print("-------------------------------------------")
    # -----------普通牌型-------------------
    # todo:连对
    def is_tcpair(self):
        cnt = 0
        nums = []
        for i in range(len(self.cnt_num)):
            if self.cnt_num[i] == 2:
                cnt += 1
                nums.append(i)
        if len(nums) == 2 and abs(nums[0] - nums[1]) == 1:
            return max(nums)
        else:
            return False

    def is_junk(self):
        return max(self.card, key=takeSecond)[1]

    # 一对
    def is_pair(self):
        for i in range(len(self.cnt_num)):
            if self.cnt_num[i] == 2:
                return i
        return False

    # 两对
    def is_tpair(self):
        cnt = 0
        max_num = -1
        for i in range(len(self.cnt_num)):
            if self.cnt_num[i] == 2:
                cnt += 1
                max_num = (i if (i > max_num) else max_num)
        if cnt == 2:
            return max_num
        return False

    # 先判断葫芦,避免判断成三条
    def is_triple(self):
        for i in range(len(self.cnt_num)):
            if self.cnt_num[i] == 3:
                return i
        return False

    # 顺子
    def is_straight(self):
        for i in range(len(self.card) - 1):

            if self.card[i][1] + 1 != self.card[i + 1][1]:
                return False
        return self.card[len(self.card) - 1][1]

    # 判断五张牌的同花
    def is_TongHua(self):
        for i in self.cnt_color:
            if i == 5:
                return max(self.card, key=takeSecond)[1]
        return False

    # 葫芦
    def is_HuLu(self):
        two = False
        three = False
        index = 0
        for i in range(0, len(self.cnt_num)):
            if self.cnt_num[i] == 2:
                two = True
            if self.cnt_num[i] == 3:
                index = i
                three = True
        if three and two:
            return index
        else:
            return False

    # 炸弹
    def is_ZhaDan(self):
        for i in range(len(self.cnt_num)):
            if self.cnt_num[i] >= 4:
                return i
        return False

    # 同花顺
    def is_TongHuaShun(self):
        return self.is_TongHua() and self.is_straight()

    # ----------------特殊牌型----------------

    def is_Dragon(self):
        # 包含两种
        # print(self.card)
        for i in self.cnt_num:
            if i > 1:
                return False
        return True

    # 12大牌
    def is_12Huang(self):
        cnt = 0
        for i in self.card:
            if i[1] <= 10:
                cnt += 1
        if cnt > 1:
            return False
        else:
            return True

    # 3炸弹
    def is_3zhadan(self):
        cnt = 0
        for i in self.cnt_num:
            if i >= 4:
                cnt += 1
        return cnt == 3

    def is_all_big(self):
        for i in self.card:
            if i[1] < 8:
                return False
        return True

    def is_all_small(self):
        for i in self.card:
            if i[1] > 8:
                return False
        return True

    # 凑一色
    def is_tcolor(self):
        return self.cnt_color[0] + self.cnt_color[2] == 13 or self.cnt_color[1] + self.cnt_color[2] == 13

    # 三同花顺
    def is_3tonghuashun(self):
        color_list = [0, 1, 2, 3]
        index = 0
        # 三色
        if self.cnt_color.count(0) != 1:
            return False
        for i in self.cnt_color:
            if i == 0:
                del color_list[index]
                break;
            index += 1
        # 三颜色
        card0 = []
        card1 = []
        card2 = []
        for c in self.card:
            if c[0] == color_list[0]:
                card0.append(c)
            if c[0] == color_list[1]:
                card1.append(c)
            if c[0] == color_list[2]:
                card2.append(c)
        print(card2)
        print(card1)
        print(card0)
        c0 = Card(card0)
        c1 = Card(card1)
        c2 = Card(card2)
        return c0.is_straight() and c1.is_straight() and c2.is_straight()

    # 三同花
    def is_same_color(self):
        for i in self.cnt_color:
            if i == 13:
                return True
        return False

    # todo
    def is_3straight(self):
       return False



    # 双怪冲三 指的是 2 对葫芦 +1 个对子 任意 1 张杂牌   两个3,3个2
    # 四套三条 指的是 4 套相同的三张牌 任意 1 张杂牌     四个3
    # 五对三条 指的是 5 个对子 3 张相同的牌        五个2,一个3
    # 六对半# 指的是# 6 个对子 任意 1 张杂牌          6个2

    # 测试
    def is_tttt(self):
        two = 0
        three = 0
        for i in self.cnt_num:
            if i == 2:
                two += 1
            if i == 3:
                three += 1
        return (two == 3 and three == 2) or (three == 4) or (two == 5 and three == 1) or (two == 6)


# list = [(1, 2), (1, 3), (1, 4), (1, 6), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11), (1, 12), (1, 13), (1, 14)]
# list = [(2, 7), (2, 5), (2, 6), (2, 4), (2, 8), (1, 3), (1, 4), (1, 6), (1, 5), (1, 7), (0, 7), (0, 5), (0, 6)]
list = [(1, 2), (1, 3), (1, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (1, 9), (1, 10), (1, 11), (1, 12), (1, 13)]
if __name__ == '__main__':
    c = Card(list)

    print(c.is_3tonghuashun())
