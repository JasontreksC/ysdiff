import pandas as pd
import pygame
from quiz import Quiz
from pygame import Vector2

class ResourceManager():
    quiz_list: list[Quiz] = [] # 창고

    ## 게임 진행 정보
    level_selected = 0
    current_chapter = 1
    
    def generate_quiz(self, chapter_count: int):
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
            # 이미지 크기 비율 = 화면 가로 길이의 절반 / 원본 이미지 가로 길이
            # => 이미지 한장이 화면 절반 만큼 줄어듦
            # => 절반보다 조금 더 줄여서 여백 표시 
            w, h = original_image.get_size()
            scale_ratio = (screen_width / 2.2) / w
            fixed_scale = (w * scale_ratio, h * scale_ratio)

            # 오리지널 이미지 크기 조절
            scaled_original_image = pygame.transform.smoothscale(original_image, fixed_scale)
            # 수정된 이미지 크기 조절
            scaled_modified_images = []
            for m in modified_images:
                scaled_modified_images.append(pygame.transform.smoothscale(m, fixed_scale))
            
            # 크기 조절된 이미지를 리스트에 저장
            new_quiz = Quiz(
                scaled_original_image,
                scaled_modified_images,
                ch_num,
                answer_df[(answer_df['chapter']==ch_num)].copy(),
                scale_ratio,
                fixed_scale
            )
            self.quiz_list.append(new_quiz)
        
    def next_level(self):
        # 다음 레벨 = (현재 레벨 + 1) % 3
        next_level = (self.level_selected + 1) % 3
        self.level_selected = next_level

    def next_chapter(self):
        self.current_chapter += 1
        
        if self.current_chapter >= 10:
            self.current_chapter = 10

    def start_chapter(self):
        self.quiz_list
        self.current_chapter = 1
        for quiz in self.quiz_list:
            quiz.flush()

    def get_current_quiz(self):
        return self.quiz_list[ self.current_chapter - 1 ]

    def get_selected_level(self):
        return self.level_selected

    def get_current_chapter(self):
        return self.current_chapter
    
resource_manager = ResourceManager()
                  