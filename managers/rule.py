import pygame
from quiz import Quiz
from pygame import Vector2

# 점수 배점
# 난이도 하: 10 * 3 = 30
# 난이도 중: 20 * 2 = 40
# 난이도 상: 50 * 1 = 50

# 난이도 0, 1, 2
# 점수  10 20 50 int
# arr[0]

class RuleManager():
    # 점수 값을 담는 속성
    SCORES = (10, 20, 50)

    # 시간 제한 (초 단위)
    time_limit = 180.0
    # 현재 남은 시간
    time_left = 0.0
    # 점수
    total_score = 0
    # 타이머가 진행중인지
    is_timer_on = False

    # 타이머 시간 줄어드는 함수 (run_ingame_state 안에서 매번 호출)
    def elapse_time(self, deltaTime: float):
        self.time_left -= deltaTime

    # 점수 올리는 함수
    def add_score(self, level: int):
        self.total_score += self.SCORES[level]

    def get_score(self):
        return self.total_score

    def reset(self):
        # 현재 남은 시간
        self.time_left = self.time_limit
        # 점수
        self.total_score = 0
        # 타이머가 진행중인지
        self.is_timer_on = True

    def timer_off(self):
        self.is_timer_on = False

    def get_timer(self):
        return round(self.time_left, 1)

rule_manager = RuleManager()