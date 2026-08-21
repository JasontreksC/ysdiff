import pygame, pygame_gui
from pygame import Surface
from managers.ui import ui_manager, check_quit

return_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((500, 800),(700, 900)),
    text='Back to title',
    manager=ui_manager,
    visible=False
)

ui_manager.regist_ui('end', return_button)

def run_end_state(dt: float, screen: Surface) -> str:
    next_state = 'end'

    for event in pygame.event.get():
        # UI매니저가 버튼 클릭 시 발생하는 모든 이벤트들을 가져와서 적용
        
        ui_manager.process_events(event)

        # 게임 종료 이벤트면
        if check_quit(event):
            next_state = 'quit'
            
        # UI 버튼 클릭 시
        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            # 클릭된 버튼이 return_button이면
            if event.ui_element == return_button:
                # 종료 화면-> 타이틀 화면으로 돌아가기
                next_state = 'title'
                ui_manager.hide_ui_pool('end')
                ui_manager.show_ui_pool('title')

                

    # 업데이트, 드로우 ...
    screen.fill((221, 189, 213))

    # ui_manager.update(dt)
    # ui_manager.draw_ui(screen)

                
    return next_state
    