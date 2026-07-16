import pygame
from pygame import Surface
from pygame.math import Vector2
from pandas import DataFrame

class Quiz:
    left_image: Surface
    right_image: Surface
    chapter: int
    answers: DataFrame
    found_indices: set  # 맞춘 정답의 DataFrame 인덱스

    # 위치, 크기 정보
    scale_ratio: float
    left_top: Vector2

    # 생성자 메소드
    def __init__(
            self,
            left_image: Surface,
            right_image: Surface,
            chapter: int,
            answers: DataFrame,
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

        # 맞춘 정답 인덱스 집합 초기화
        self.found_indices = set()

    # 정답 판정 메소드 (좌표 클릭 시 호출)
    def check_answer(self, click_pos: Vector2, level: int):
        # 기본 허용 범위 반경을 10픽셀로
        # 반경이 겹치면 가까운걸 우선으로
        # 반경 내 정답들을 거리와 함께 삽입 후 거리순 정렬, 맨앞 하나를 pop
        RADIUS = 10
        current_level_answer = self.answers[self.answers['level'] == level]

        candidates = []
        for idx, row in current_level_answer[["x_pos", "y_pos"]].iterrows():
            if idx in self.found_indices:
                continue
            answer_pos = Vector2(row['x_pos'], row['y_pos'])
            screen_pos_left = self.left_top + answer_pos * self.scale_ratio
            screen_pos_right = self.left_top + Vector2(self.left_image.get_width(), 0) + answer_pos * self.scale_ratio

            dist = min(click_pos.distance_to(screen_pos_left), click_pos.distance_to(screen_pos_right))
            if dist <= RADIUS:
                candidates.append((dist, idx))

        if candidates:
            candidates.sort(key=lambda x: x[0])
            _, closest_idx = candidates[0]
            self.found_indices.add(closest_idx)

    def draw(self, screen: Surface, screen_height: int):
        # 왼쪽 이미지 띄우기 (좌측 상단)
        screen.blit(self.left_image, self.left_top)
        # 오른쪽 이미지 띄우기 (죄측 상단 + 이미지 가로 길이)
        screen.blit(self.right_image, self.left_top + Vector2(self.left_image.get_width(), 0))

        # 맞춘 정답이 있는 경우 해당 위치에 원 그리기
        for idx in self.found_indices:
            row = self.answers.loc[idx]
            answer_pos = Vector2(row['x_pos'], row['y_pos'])
            # 정답 위치 원 그리기 (좌측 상단 + 정답 좌표)
            pygame.draw.circle(screen, (0, 255, 0), self.left_top + answer_pos * self.scale_ratio, 10)
            # 정답 위치 원 그리기 (좌측 상단 + 이미지 가로 길이 + 정답 좌표)
            pygame.draw.circle(screen, (0, 255, 0), self.left_top + Vector2(self.left_image.get_width(), 0) + answer_pos * self.scale_ratio, 10)