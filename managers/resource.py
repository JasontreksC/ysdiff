import pandas as pd
import pygame
from quiz import Quiz
from pygame import Vector2
from PIL import Image

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

        ORIGINAL_SIZE = (3024, 4032)

        # ch_num이 1에서 10까지 반복
        for ch_num in range(1, chapter_count + 1): # 공장
            # 이미지 리사이즈 크기 계산
            w, h = ORIGINAL_SIZE
            scale_ratio = (screen_width / 2.2) / w
            fixed_scale = (round(w * scale_ratio), round(h * scale_ratio))

            # 오리지널 이미지 불러오기
            original_pil = Image.open(f'images/ysu_ch{ch_num}_original.png').convert("RGB")
            original_pil = original_pil.resize(fixed_scale, Image.Resampling.LANCZOS)
            original_image = pygame.image.frombytes(original_pil.tobytes(), original_pil.size, "RGB").convert()
            # 수정된 이미지 불러오기
            modified_images = []
            for i in range(0, 3):
                modified_pil = Image.open(f'images/ysu_ch{ch_num}_{i}.png').convert("RGB")
                modified_pil = modified_pil.resize(fixed_scale, Image.Resampling.LANCZOS)
                modified_images.append(pygame.image.frombytes(modified_pil.tobytes(), modified_pil.size, "RGB").convert())
            
            
            # 크기 조절된 이미지를 리스트에 저장
            new_quiz = Quiz(
                original_image,
                modified_images,
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

    def reload_answers(self):
        answer_df = pd.read_csv("answers.csv", encoding="utf-8-sig")
        self.get_current_quiz().answers = answer_df[(answer_df['chapter']==self.get_current_chapter())].copy()

resource_manager = ResourceManager()
                  