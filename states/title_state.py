import pygame, pygame_gui
from pygame import Surface

from managers.ui import ui_manager, check_quit

from managers.resource import select_level

test_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((0, 0),(200, 100)),
    text='테스트 버튼',
    manager=ui_manager
)

def run_title_state(dt: float, screen: Surface) -> str:
    next_state = 'title'

    # 이벤트 처리 (한번만 실행해야 하는 코드)
    for event in pygame.event.get():
        # UI매니저가 버튼 클릭 시 발생하는 모든 이벤트들을 가져와서 적용
        ui_manager.process_events(event)

        # 게임 종료 이벤트면
        if check_quit(event):
            next_state = 'quit'

        # UI 버튼 클릭 시
        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            # 클릭된 버튼이 test_button이면
            if event.ui_element == test_button:
                # 타이틀 화면 -> 인게임 화면 넘어가기
                next_state = 'ingame'

    screen.fill((221, 189, 213))

    ui_manager.update(dt)
    ui_manager.draw_ui(screen)

    return next_state