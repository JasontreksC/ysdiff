# ingame_state.py
# 실제 게임 로직
# 우리가 밖에다 놨던 이미지 띄우기, 클릭시 정답 처리 등등을 여기서

import pygame, pygame_gui
from pygame import Surface, Vector2
from managers.ui import ui_manager, check_quit
from managers.resource import resource_manager
from managers.rule import rule_manager

chapter_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((0, -460),(1000, 150)),
    text='현재 챕터: 1/10 | 맞춘 정답 수: 0/3',
    manager=ui_manager,
    visible=False,
    anchors={'center':'center'},
    object_id='#subtitle'
)

to_next_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((0, 460),(1000, 150)),
    text='다음으로 넘어가기: 스페이스 바 | 게임 끝내기: 백 스페이스',
    manager=ui_manager,
    visible=False,
    anchors={'center':'center'},
    object_id='#subtitle'
)

score_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((400, -460),(1000, 150)),
    text='현재 점수: 0',
    manager=ui_manager,
    visible=False,
    anchors={'center':'center'},
    object_id='#subtitle'
)

timer_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((-400, -460),(1000, 150)),
    text='남은 시간: 0초',
    manager=ui_manager,
    visible=False,
    anchors={'center':'center'},
    object_id='#subtitle'
)

ui_manager.regist_ui('ingame', chapter_label, to_next_label, score_label, timer_label)

def run_ingame_state(dt: float, screen: Surface) -> str:

    next_state = 'ingame'
    # Quiz 객체, 선택된 난이도, 현재 챕터 정보를 ResourceManager라는 주인에게 받아옴
    current_quiz = resource_manager.get_current_quiz()
    level_selected = resource_manager.get_selected_level()
    current_chapter = resource_manager.get_current_chapter()

    # 맞춘 정답 개수 조회
    total_count = 3 - level_selected
    found_count = len(current_quiz.found_indices)

    # 시간 소모
    rule_manager.elapse_time(dt)

    
    # 이벤트 처리 (한번만 실행해야 하는 코드)
    for event in pygame.event.get():
        # UI매니저가 버튼 클릭 시 발생하는 모든 이벤트들을 가져와서 적용

        # 게임 종료 이벤트면
        if check_quit(event):
            next_state = 'quit'

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            ww, wh = pygame.display.get_window_size()
            sw, sh = screen.get_size()
            click = Vector2(mx * sw / ww, my * sh / wh)
            is_answer = current_quiz.check_answer(click, level_selected)
            if is_answer:
                rule_manager.add_score(level_selected)
            
        # 스페이스바: 다음 챕터, 마지막 챕터면 결과 화면
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if current_chapter >= 10:
                    next_state = 'end'
                    ui_manager.hide_ui_pool('ingame')
                    ui_manager.show_ui_pool('end')
                else:
                    resource_manager.next_chapter()
            elif event.key == pygame.K_BACKSPACE:
                next_state = 'end'
                ui_manager.hide_ui_pool('ingame')
                ui_manager.show_ui_pool('end')

    chapter_label.set_text(f'현재 챕터: {resource_manager.current_chapter}/10 | 맞춘 정답 수: {found_count}/{total_count}')
    score_label.set_text(f'현재 점수: {rule_manager.get_score()}')
    timer_label.set_text(f'남은 시간: {rule_manager.get_timer()}초')

    screen.fill((221, 189, 213))


    current_quiz.draw(screen, level_selected)

    return next_state