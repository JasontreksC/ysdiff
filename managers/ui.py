import pygame, pygame_gui

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

class UIManager(pygame_gui.UIManager):

    ui_pools: dict[str, list] = {}

    def regist_ui(self, pool_name: str, *uis):
        if not pool_name in self.ui_pools.keys():
            self.ui_pools[pool_name] = []

        for ui in uis:
            self.ui_pools[pool_name].append(ui)

    def show_ui_pool(self, pool_name: str):
        if not pool_name in self.ui_pools.keys():
            return

        for ui in self.ui_pools[pool_name]:
            ui.show()

    def hide_ui_pool(self, pool_name: str):
            if not pool_name in self.ui_pools.keys():
                return
    
            for ui in self.ui_pools[pool_name]:
                ui.hide()

# 화면 정보 가져오기
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

# UI 매니저 생성
ui_manager = UIManager((screen_width, screen_height), theme_path='theme/theme.json')
