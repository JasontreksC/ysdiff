import pygame, pygame_gui
from pygame import Surface, Vector2

from managers.ui import ui_manager, check_quit

from managers.resource import resource_manager

game_title = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((0, -200),(1000, 150)),
    text='연성대 배경 틀린그림 찾기',
    manager=ui_manager,
    visible=False,
    anchors={'center':'center'},
    object_id='#title'
)

game_subtitle = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((0, -120),(1000, 150)),
    text='우리 학교 사진속에서 틀린부분을 찾아보세요!',
    manager=ui_manager,
    visible=False,
    anchors={'center':'center'},
    object_id='#subtitle'
)

start_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((0, 0),(300, 150)),
    text='게임 시작!',
    manager=ui_manager,
    visible=False,
    anchors={'center':'center'},
    object_id='#start_button'

)
level_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((0, 300),(200, 100)),
    manager=ui_manager,
    text='',
    visible=False,
    anchors={'center':'center'}
)

ui_manager.regist_ui('title', game_title, game_subtitle, start_button, level_button)

def run_title_state(dt: float, screen: Surface) -> str:
    # 선택된 레벨 가져오기
    level = ['하', '중', '상']
    level_button.set_text(f'난이도: {level[resource_manager.get_selected_level()]}')

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
            if event.ui_element == start_button:
                # 타이틀 화면 -> 인게임 화면 넘어가기
                next_state = 'ingame'
                resource_manager.start_chapter()
                ui_manager.hide_ui_pool('title')

            # Level 버튼 클릭시 난이도 변경
            if event.ui_element == level_button:
                resource_manager.next_level() 

    screen.fill((221, 189, 213))

    return next_state