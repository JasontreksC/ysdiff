import pygame, pygame_gui
from pygame import Surface, Vector2
from quiz import Quiz
import pandas as pd


# 초기화
pygame.init()
# 시간 측정기
clock = pygame.time.Clock()
# 화면 정보 가져오기
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
# 게임 화면 설정
screen = pygame.display.set_mode(
    (screen_width, screen_height), 
    pygame.FULLSCREEN | pygame.SCALED, 
    vsync=1

)

from states.title_state import run_title_state


def main():
    running = True
    chapter_count = 10
    current_chapter = 1
    
    # 여기서 레벨 선택

    level_selected = 0 # 하:0, 중:1, 상:2

    # 퀴즈들을 담을 리스트
    quiz_list: list[Quiz] = []

    # 정답들을 담을 DataFrame
    answer_df = pd.read_csv("answers.csv", encoding="utf-8-sig")

    # ch_num이 1에서 10까지 반복
    for ch_num in range(1, chapter_count + 1):
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

    # 처음에는 타이틀 화면
    game_state = 'title'

    while game_state != 'quit':
        deltaTime = clock.tick() / 1000.0

        # 현재 보여주는 퀴즈
        current_quiz = quiz_list[current_chapter - 1]

        # 게임 진행 상황에 따른 분기
        match game_state:
            # 타이틀 화면일 때
            case 'title':
                game_state = run_title_state(deltaTime, screen)
            # 게임 진행 중일 때
            case 'ingame':
                print('인게임 화면입니다.')
            # 게임 종료 화면일 때
            case 'end':
                pass

        # 렌더링(화면 출력)
        pygame.display.flip()

    pygame.quit()

main()