import pygame, pygame_gui

# 화면 정보 가져오기
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

# UI 매니저 생성
ui_manager = pygame_gui.UIManager((screen_width, screen_height))

# 게임 종료 조건 (ESC 누름, 창 닫기) 검사
def check_quit(event: pygame.Event) -> bool:
    # 창 X버튼 눌렀을 때 종료
    if event.type == pygame.QUIT:
        return True
    # ESC 키 눌렀을 때 종료
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            return True
    # 어떤 종료 조건도 없음(게임 유지)
    return False