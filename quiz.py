import pygame
from pygame import Surface
from pygame.math import Vector2

class Quiz:
    left_image: Surface
    right_image: Surface
    chapter: int
    answers: list[Vector2]

    # 위치, 크기 정보
    scale_ratio: float
    left_top: Vector2

    # 생성자 메소드
    def __init__(
            self, 
            left_image: Surface, 
            right_image: Surface, 
            chapter: int, 
            answers: list[Vector2],
            scale_ratio: float,
            left_top: Vector2
        ):
        # 이미지(L, R), 챕터 번호, 정답 좌표들을 매개변수로 받아서 저장
        self.left_image = left_image
        self.right_image = right_image
        self.chapter = chapter
        self.answers = answers

        # 크기 비율 저장
        self.scale_ratio = scale_ratio
        # 왼쪽 이미지가 그려질 위치
        self.left_top = left_top

    def draw(self, screen: Surface, screen_height: int):
        # 왼쪽 이미지 띄우기 (좌측 상단)
        screen.blit(self.left_image, self.left_top)
        # 오른쪽 이미지 띄우기 (죄측 상단 + 이미지 가로 길이)
        screen.blit(self.right_image, self.left_top + Vector2(self.left_image.get_width(), 0))

    def draw_answer(self, screen: Surface):
        for answer in self.answers:
            # 정답 위치 원 그리기 (좌측 상단 + 정답 좌표)
            pygame.draw.circle(screen, (255, 0, 0), self.left_top + answer * self.scale_ratio, 10)
            # 정답 위치 원 그리기 (좌측 상단 + 이미지 가로 길이 + 정답 좌표)
            pygame.draw.circle(screen, (255, 0, 0), self.left_top + Vector2(self.left_image.get_width(), 0) + answer * self.scale_ratio, 10)