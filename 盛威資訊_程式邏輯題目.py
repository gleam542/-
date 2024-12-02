"""使用python 3.13.0"""

### 程式邏輯題目 ###
#1
def correct_scores(wrong_scores):
    """
    修正老師輸入錯誤的成績，將數字反轉回正確的成績。

    :param wrong_scores: List[int] 老師輸入錯誤的成績列表
    :return: List[int] 修正後的成績列表
    """
    corrected_scores = [int(str(score)[::-1]) for score in wrong_scores]
    return corrected_scores

#2
def count_letters(text):
    """
    計算文字中每個字母的出現次數，大小寫視為同個字母。

    :param text: str 要計算的文字
    :return: dict 各字母出現次數的字典
    """
    # 初始化一個空字典來存儲字母計數
    letter_counts = {}

    # 將所有字母轉為小寫，並過濾非字母字元
    for char in text.lower():
        if char.isalpha():
            if char in letter_counts:
                letter_counts[char] += 1
            else:
                letter_counts[char] = 1

    return letter_counts

#3
def last_person_standing(n):
    """
    計算最後留下的人是第幾順位。

    :param n: int 總人數
    :return: int 最後留下的人的順位
    """
    people = list(range(1, n + 1))  # 初始化圈子
    index = 0  # 起始報數位置

    while len(people) > 1:
        index = (index + 2) % len(people)  # 報到3的人退出
        print(f"報數到3的人: {people[index]} (退出)")  # 調試輸出
        people.pop(index)
        print(f"剩餘人員: {people}")  # 調試輸出

    return people[0]  # 返回最後留下的人的順位



