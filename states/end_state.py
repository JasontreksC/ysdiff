import pygame, pygame_gui
from pygame import Surface
from managers.ui import ui_manager, check_quit
from managers.resource import resource_manager
from managers.rule import rule_manager

result_time_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((0, -100),(1000, 300)),
    text='소모 시간: 0초',
    manager=ui_manager,
    visible=False,
    anchors={'center':'center'},
    object_id='#title'
)

result_answer_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((0, 0),(1000, 300)),
    text='맞춘 정답 수: 0개',
    manager=ui_manager,
    visible=False,
    anchors={'center':'center'},
    object_id='#title'
)

result_score_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((0, 100),(1000, 300)),
    text='최종 점수: 0점',
    manager=ui_manager,
    visible=False,
    anchors={'center':'center'},
    object_id='#title'
)

return_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((0, 350),(400, 150)),
    text='타이틀로 돌아가기',
    manager=ui_manager,
    visible=False,
    anchors={'center':'center'},
    object_id='#start_button'
)

ui_manager.regist_ui('end', result_score_label, result_time_label, result_answer_label, return_button)

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

    result_time_label.set_text(f'소모 시간: {round(rule_manager.time_limit - rule_manager.get_timer(), 1)}초')
    result_answer_label.set_text(f'맞춘 정답 수: {resource_manager.get_final_answer_count()}개')
    result_score_label.set_text(f'최종 점수: {rule_manager.get_score()}점')

    # 업데이트, 드로우 ...
    screen.fill((221, 189, 213))

                
    return next_state
    