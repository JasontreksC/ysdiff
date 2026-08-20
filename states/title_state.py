import pygame, pygame_gui
from pygame import Surface

from managers.ui import ui_manager, check_quit

from managers.resource import resource_manager

start_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((0, 0),(200, 100)),
    text='테스트 버튼',
    manager=ui_manager,
    visible=False

)
level_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((250, 100),(450, 200)),
    manager=ui_manager,
    text='',
    visible=False
)

def run_title_state(dt: float, screen: Surface) -> str:
    # 선택된 레벨 가져오기
    level_selected = resource_manager.get_selected_level()
    level_button.set_text(f'level {level_selected}')

    next_state = 'title'
    start_button.show()
    level_button.show()
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
            if event.ui_element == start_button:
                # 타이틀 화면 -> 인게임 화면 넘어가기
                next_state = 'ingame'
                start_button.hide()
                level_button.hide()
                resource_manager.start_chapter()

            if event.ui_element == level_button:
                resource_manager.next_level() 

    screen.fill((221, 189, 213))

    ui_manager.update(dt)
    ui_manager.draw_ui(screen)

    return next_state