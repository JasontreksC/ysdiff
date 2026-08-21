# ingame_state.py
# 실제 게임 로직
# 우리가 밖에다 놨던 이미지 띄우기, 클릭시 정답 처리 등등을 여기서

import pygame
from pygame import Surface, Vector2

from managers.ui import ui_manager, check_quit

from managers.resource import resource_manager

def run_ingame_state(dt: float, screen: Surface) -> str:

    next_state = 'ingame'
    # Quiz 객체, 선택된 난이도, 현재 챕터 정보를 ResourceManager라는 주인에게 받아옴
    current_quiz = resource_manager.get_current_quiz()
    level_selected = resource_manager.get_selected_level()
    current_chapter = resource_manager.get_current_chapter()
    
    # 이벤트 처리 (한번만 실행해야 하는 코드)
    for event in pygame.event.get():
        # UI매니저가 버튼 클릭 시 발생하는 모든 이벤트들을 가져와서 적용

        # 게임 종료 이벤트면
        if check_quit(event):
            next_state = 'quit'

        elif event.type == pygame.MOUSEBUTTONDOWN:
            resource_manager.reload_answers()
            current_quiz.check_answer(Vector2(event.pos), level_selected)


    screen.fill((221, 189, 213))


    current_quiz.draw(screen, level_selected)
    #    난이도 정답갯수
    # 하    0    3      현재 퀴즈 정답 갯수 >= 3 - 0
    # 중    1    2                         3 - 1
    # 상    2    1                         3 - 2

    # 정답을 다 맞췄을 때 -> 마지막 챕터인지
    if len(current_quiz.found_indices) >= 3 - level_selected:
        # 마지막 챕터라면 -> 다음 게임 상태를 "end"로
        if current_chapter >= 10:
            next_state = 'end'
            ui_manager.show_ui_pool('end')
        else:
            resource_manager.next_chapter()

    return next_state