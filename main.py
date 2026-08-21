import pygame, pygame_gui
from pygame import Surface, Vector2
from quiz import Quiz
import pandas as pd

# 파이게임 초기화
pygame.init()

# 매니저 생성
from managers.resource import resource_manager
from managers.ui import ui_manager


# 시간 측정기
clock = pygame.time.Clock()
# 화면 정보 가져오기
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
# 게임 화면 설정
screen = pygame.display.set_mode(
    (screen_width, screen_height), 
    pygame.FULLSCREEN, 
    vsync=1
)

from states.title_state import run_title_state
from states.ingame_state import run_ingame_state
from states.end_state import run_end_state
def main():
    running = True
    chapter_count = 10

    # 퀴즈 공장 가동
    resource_manager.generate_quiz(chapter_count)

    # 처음에는 타이틀 화면
    game_state = 'title'
    ui_manager.show_ui_pool('title')

    while game_state != 'quit':
        deltaTime = clock.tick() / 1000.0

        # 게임 진행 상황에 따른 분기
        match game_state:
            # 타이틀 화면일 때
            case 'title':
                game_state = run_title_state(deltaTime, screen)
            # 게임 진행 중일 때
            case 'ingame':
                game_state = run_ingame_state(deltaTime, screen)
            # 게임 종료 화면일 때
            case 'end':
                game_state = run_end_state(deltaTime, screen)

        # UI 출력
        ui_manager.update(deltaTime)
        ui_manager.draw_ui(screen)
        # 렌더링(화면 출력)
        pygame.display.flip()

    pygame.quit()

main()