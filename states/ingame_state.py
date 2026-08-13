# ingame_state.py
# 실제 게임 로직
# 우리가 밖에다 놨던 이미지 띄우기, 클릭시 정답 처리 등등을 여기서

import pygame, pygame_gui
from pygame import Surface, Vector2

from managers.ui import check_quit

from quiz import Quiz

from managers.resource import quiz_list, level_selected, next_chapter

def run_ingame_state(dt: float, screen: Surface) -> str:

    from managers.resource import current_chapter

    next_state = 'ingame'
    current_quiz = quiz_list[current_chapter - 1]

    # 이벤트 처리 (한번만 실행해야 하는 코드)
    for event in pygame.event.get():
        # UI매니저가 버튼 클릭 시 발생하는 모든 이벤트들을 가져와서 적용

        # 게임 종료 이벤트면
        if check_quit(event):
            next_state = 'quit'

        elif event.type == pygame.MOUSEBUTTONDOWN:
            current_quiz.check_answer(Vector2(event.pos), level_selected)


    screen.fill((221, 189, 213))


    current_quiz.draw(screen=screen, screen_height=screen.height, difficult=level_selected)
    #    난이도 정답갯수
    # 하    0    3      현재 퀴즈 정답 갯수 >= 3 - 0
    # 중    1    2                         3 - 1
    # 상    2    1                         3 - 2

    print(f"지금까지 맞힌 정답 갯수: {len(current_quiz.found_indices)}")
    print(f"현재 챕터 번호: {current_chapter}")

    if len(current_quiz.found_indices) >= 3 - level_selected:
        next_chapter()





    return next_state