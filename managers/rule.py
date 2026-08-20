import pygame
from quiz import Quiz
from pygame import Vector2

class RuleManager():
    # 시간 제한 (초 단위)
    time_limit = 180.0
    # 현재 남은 시간
    time_left = 0.0
    # 점수
    score = 0
    # 타이머가 진행중인지
    is_timer_on = False

    # 타이머 시작(남은 시간을 설정한 제한 시간으로 설정)
    def start_timer(self):
        self.time_left = self.time_limit
        self.is_timer_on = True

    # 타이머 시간 줄어드는 함수 (run_ingame_state 안에서 매번 호출)
    def elapse_time(self, deltaTime: float):
        self.time_left -= deltaTime

    # 점수 올리는 함수
    def add_score(self, score: int):
        self.score += score
        

rule_manager = RuleManager()