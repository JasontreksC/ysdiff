import pandas as pd
import pygame
from quiz import Quiz
from pygame import Vector2

quiz_list: list[Quiz] = [] # 창고

def generate_quiz(chapter_count: int):
    # 전역 변수 사용 선언
    global quiz_list

    # 정답들을 담을 DataFrame
    answer_df = pd.read_csv("answers.csv", encoding="utf-8-sig")

    # 이미지 크기를 맞추기 위한 화면 크기 정보
    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h

    # ch_num이 1에서 10까지 반복
    for ch_num in range(1, chapter_count + 1): # 공장
        # 오리지널 이미지 불러오기
        original_image = pygame.image.load(f'images/ysu_ch{ch_num}_original.png')
        # 수정된 이미지 불러오기
        modified_images = []
        for i in range(0, 3):
            modified_images.append(pygame.image.load(f'images/ysu_ch{ch_num}_{i}.png'))
        
        # i번 이미지 불러오기 (왼쪽, 오른쪽)
        # 크기 비율 구하기
        w, h = original_image.get_size()
        scale_ratio = (screen_width / 2) / w
        # 오리지널 이미지 크기 조절
        scaled_original_image = pygame.transform.smoothscale(
            original_image, (w * scale_ratio, h * scale_ratio)
        )
        # 수정된 이미지 크기 조절
        scaled_modified_images = []
        for m in modified_images:
            scaled_modified_images.append(
                pygame.transform.smoothscale(m, (w * scale_ratio, h * scale_ratio))
            )
        
        # 크기 조절된 이미지를 리스트에 저장
        new_quiz = Quiz(
            scaled_original_image,
            scaled_modified_images,
            ch_num,
            answer_df[(answer_df['chapter']==ch_num)].copy(),
            scale_ratio,
            Vector2(0, screen_height / 2 - scaled_original_image.get_height() / 2)
        )
        quiz_list.append(new_quiz)

## 게임 진행 정보
level_selected = 0
current_chapter = 1

## 정보 업데이트 함수
def select_level(level: int):
    global level_selected
    level_selected = level

def next_chapter():
    global current_chapter
    current_chapter += 1