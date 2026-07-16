import pygame, csv
from pygame import Surface, Vector2
from quiz import Quiz
from PIL import Image, ImageOps

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
    current_chapter = 1

    # 퀴즈들을 담을 리스트
    quiz_list: list[Quiz] = []
    image_count = 1

    # 정답들을 담을 딕셔너리
    answers: dict[int, list[Vector2]] = {}

    with open("answers.csv", "r", encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        for row in reader:
            # 만약 챕터 번호(키값)가 키에 없으면 (처음 삽입하는 키값이면)
            if not int(row[0]) in answers.keys():
                # 빈 배열을 넣어서 초기화
                answers[int(row[0])] = []
            # 챕터 번호(키값)으로 찾은 배열에 정답 좌표 추가
            answers[int(row[0])].append(Vector2(int(row[1]), int(row[2])))

    for i in range(1, image_count + 1):
        # 왼쪽 이미지 불러오기
        left_image = Image.open(f"images/ysu{i}_L.jpg")
        left_image = ImageOps.exif_transpose(left_image)
        # 오른쪽 이미지 불러오기
        right_image = Image.open(f"images/ysu{i}_R.jpg")
        right_image = ImageOps.exif_transpose(right_image)
        # i번 이미지 불러오기 (왼쪽, 오른쪽)
        left_surface = pygame.image.frombytes(left_image.tobytes(), left_image.size, left_image.mode)
        right_surface = pygame.image.frombytes(right_image.tobytes(), right_image.size, right_image.mode)
        # 크기 비율 구하기
        w, h = left_surface.get_size()
        scale_ratio = (screen_width / 2) / w
        # 크기 조절
        scaled_left_surface = pygame.transform.scale(left_surface, (w * scale_ratio, h * scale_ratio))
        scaled_right_surface = pygame.transform.scale(right_surface, (w * scale_ratio, h * scale_ratio))
        # 크기 조절된 이미지를 리스트에 저장
        new_quiz = Quiz(
            scaled_left_surface,
            scaled_right_surface,
            i,
            answers[i],
            scale_ratio,
            Vector2(0, screen_height / 2 - scaled_left_surface.get_height() / 2)
        )
        quiz_list.append(new_quiz)


    while running:
        deltaTime = clock.tick() / 1000.0

        # 이벤트 처리 (한번만 실행해야 하는 코드)
        for event in pygame.event.get():
            # 창 X버튼 눌렀을 때 종료
            if event.type == pygame.QUIT:
                running = False
            # ESC 키 눌렀을 때 종료
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        ## 배경 화면 채우기
        screen.fill((30, 30, 30))

        # 퀴즈 출력
        quiz_list[current_chapter - 1].draw(screen, screen_height)
        # 정답 출력
        quiz_list[current_chapter - 1].draw_answer(screen)

        # 키 입력받기
        keys = pygame.key.get_pressed()
        

        # 렌더링(화면 출력)
        pygame.display.flip()

    pygame.quit()

main()