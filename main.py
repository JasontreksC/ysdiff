import pygame, csv
from pygame import Surface, Vector2
from quiz import Quiz
import pandas as pd

# 초기화
pygame.init()
# 시간 측정기
clock = pygame.time.Clock()
# 화면 정보 가져오기
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
# 게임 화면 설정
screen = pygame.display.set_mode(
    (screen_width, screen_height), 
    pygame.FULLSCREEN | pygame.SCALED, 
    vsync=1
)

def main():
    running = True
    chapter_count = 10
    current_chapter = 1
    
    # 여기서 레벨 선택

    level_selected = 0 # 하:0, 중:1, 상:2

    # 퀴즈들을 담을 리스트
    quiz_list: list[Quiz] = []

    # 정답들을 담을 DataFrame
    answer_df = pd.read_csv("answers.csv", encoding="utf-8-sig")

    # ch_num이 1에서 10까지 반복
    for ch_num in range(1, chapter_count + 1):
        # 왼쪽 이미지 불러오기
        left_surface = pygame.image.load(f'images/ysu_ch{ch_num}_L.png')
        # 오른쪽 이미지 불러오기
        right_surface = pygame.image.load(f'images/ysu_ch{ch_num}_R.png')
        # i번 이미지 불러오기 (왼쪽, 오른쪽)
        # 크기 비율 구하기
        w, h = left_surface.get_size()
        scale_ratio = (screen_width / 2) / w
        # 크기 조절
        scaled_left_surface = pygame.transform.smoothscale(left_surface, (w * scale_ratio, h * scale_ratio))
        scaled_right_surface = pygame.transform.smoothscale(right_surface, (w * scale_ratio, h * scale_ratio))
        # 크기 조절된 이미지를 리스트에 저장
        new_quiz = Quiz(
            scaled_left_surface,
            scaled_right_surface,
            ch_num,
            answer_df[(answer_df['chapter']==ch_num)].copy(),
            scale_ratio,
            Vector2(0, screen_height / 2 - scaled_left_surface.get_height() / 2)
        )
        quiz_list.append(new_quiz)


    while running:
        deltaTime = clock.tick() / 1000.0

        # 현재 보여주는 퀴즈
        current_quiz = quiz_list[current_chapter - 1]

        # 이벤트 처리 (한번만 실행해야 하는 코드)
        for event in pygame.event.get():
            # 창 X버튼 눌렀을 때 종료
            if event.type == pygame.QUIT:
                running = False
            # ESC 키 눌렀을 때 종료
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            # 마우스 버튼 클릭 시 이벤트
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 마우스 버튼 좌표
                x, y = event.pos
                # 좌클릭 이벤트인 경우
                if event.button == 1: # 좌클릭
                    # 여기서 current_quiz 의 정답 처리 메소드 호출!
                    current_quiz.check_answer(Vector2(x, y), level_selected)

        ## 배경 화면 채우기
        screen.fill((30, 30, 30))

        # 퀴즈 출력
        current_quiz.draw(screen, screen_height)

        # 키 입력받기
        keys = pygame.key.get_pressed()
        

        # 렌더링(화면 출력)
        pygame.display.flip()

    pygame.quit()

main()