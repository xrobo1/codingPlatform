import pygame
pygame.init()




# 화면 크기 설정
화면_너비 = 400
화면_높이 = 300
화면_크기 = (화면_너비, 화면_높이)

# 화면 생성 및 최대화 버튼 활성화
screen = pygame.display.set_mode(화면_크기, pygame.RESIZABLE)

# 제목 설정
pygame.display.set_caption("원 그리기 예제")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (120, 120, 120)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 폰트 설정
폰트 = pygame.font.Font(None, 20)




BLOCK_WIDTH = 160
BLOCK_HEIGHT = 50

blocks = [
    {"color": RED, "rect": pygame.Rect(105, 70, BLOCK_WIDTH, BLOCK_HEIGHT)},
    {"color": GREEN, "rect": pygame.Rect(105, 140, BLOCK_WIDTH, BLOCK_HEIGHT)},
    {"color": BLUE, "rect": pygame.Rect(105, 210, BLOCK_WIDTH, BLOCK_HEIGHT)},
]
coding_blocks = []
dragging_block = None
dragging_start_point = (None, None)

def draw_blocks():
    for block in blocks:
        pygame.draw.rect(screen, block["color"], block["rect"])
        pygame.draw.rect(screen, WHITE, block["rect"], 2)  # border

def draw_coding_blocks():
    for block in coding_blocks:
        pygame.draw.rect(screen, block["color"], block["rect"])
        pygame.draw.rect(screen, WHITE, block["rect"], 2)  # border





def get_current_screen_size(screen):
    w, h = screen.get_width(), screen.get_height()
    return (w, h)






def handle_click(event, screen_size):
    section_name = get_screen_section_name(screen_section, screen_size, event.pos)
    
    block_holding = None
    if section_name == "header":
        handle_click_header(event)
    if section_name == "block_list":
        handle_click_block_list(event)
    elif section_name == "block_navigator":
        handle_click_block_navigator(event)
    elif section_name == "upload":
        handle_click_upload(event)
    elif section_name == "script":
        handle_click_script(event)
    else:
        print(f"Undescripted Section")

    return block_holding

def handle_click_header(event):
    section_name = "header"
    if event.type == pygame.MOUSEBUTTONDOWN:
        print(f"[{section_name}] 클릭")      
    else:
        print(f"[{section_name}] 다른 이벤트")

def handle_click_block_navigator(event):
    section_name = "block_navigator"
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 4:
            print(f"[{section_name}] 마우스 휠 위로")
        elif event.button == 5:
            print(f"[{section_name}] 마우스 휠 아래로")
        else:
            print(f"[{section_name}] 클릭")
    else:
        print(f"[{section_name}] 다른 이벤트")

def handle_click_block_list(event):
    section_name = "block_list"
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 4:
            print(f"[{section_name}] 마우스 휠 위로")
            # offset을 바꿔주는 방식
            # offset 반영해서 블록을 그리기 (휠 스크롤 한 번에 블록 한 개씩)
        elif event.button == 5:
            print(f"[{section_name}] 마우스 휠 아래로")
            # offset 반영해서 블록을 그리기 (휠 스크롤 한 번에 블록 한 개씩)
        elif event.button == 1:
            print(f"[{section_name}] 클릭")
            # offset을 체크한 후, 현재 몇번째 블록을 클릭했는지 확인
            # 일단 잡아
            block_hold = True
            if block_hold:
                handle_click_block(event)
            
    else:
        print(f"[{section_name}] 다른 이벤트")

def handle_click_block(event):
    global dragging_block, dragging_start_point
    pos = event.pos
    for block in blocks:
        if block["rect"].collidepoint(pos):
            new_block = {"color": block["color"], "rect": pygame.Rect(pos[0], pos[1], BLOCK_WIDTH, BLOCK_HEIGHT)}
            coding_blocks.append(new_block)
            dragging_block = new_block
            return
    
    for block in coding_blocks:
        if block["rect"].collidepoint(pos):
            dragging_block = block
            dragging_start_point = pos
            coding_blocks.remove(dragging_block)
            coding_blocks.append(dragging_block)
            return


def handle_drag(pos):
    if not dragging_block:
        return
    dx = pos[0] - dragging_block["rect"].centerx
    dy = pos[1] - dragging_block["rect"].centery
    dragging_block["rect"].move_ip(dx, dy)


def handle_release(event, screen_size):
    event_pos = event.pos
    section_name = get_screen_section_name(screen_section, screen_size, event.pos)

    global dragging_block, coding_blocks, dragging_start_point
    if dragging_block:
        if section_name == "block_list":
            for block in coding_blocks:
                if block == dragging_block:
                    coding_blocks.remove(block)
                    break
        elif section_name != "script":
            dragging_block["rect"].centerx = dragging_start_point[0]
            dragging_block["rect"].centery = dragging_start_point[1]
        dragging_block = None


def handle_click_upload(event):
    section_name = "upload"
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        print(f"[{section_name}] 클릭")

def handle_click_script(event):
    section_name = "script"
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 4:
            print(f"[{section_name}] 마우스 휠 위로")
        elif event.button == 5:
            print(f"[{section_name}] 마우스 휠 아래로")
        else:
            print(f"[{section_name}] 클릭")
            handle_click_block(event)
    else:
        print(f"[{section_name}] 다른 이벤트")




"""
screen을 section 별로 분리

attribute:
    - name:
        section의 이름
        event_handler에서 사용
    - pos:
        - left_top: 왼쪽 위의 좌표.
        - right_bottom: 오른쪽 아래의 좌표.
        rect를 그릴 때 시작점의 좌표와 사이즈를 계산할 때 사용
        좌표 계산 시 offset을 사용
            좌표 > 0: screen 시작점으로부터 offset
            좌표 == None: screen size만큼
            좌표 < 0: screen 끝점으로부터 offset
    - color:
        section의 색깔
"""
screen_section = [{
    "name": "header",
    "pos": {
        "left_top": (0, 0),
        "right_bottom": (None, 50)
    },
    "color": BLACK
}, {
    "name": "upload",
    "pos": {
        "left_top": (0, -100),
        "right_bottom": (300, None)
    },
    "color": BLACK
},{
    "name": "block_navigator",
    "pos": {
        "left_top": (0, 50),
        "right_bottom": (100, -100)
    },
    "color": WHITE
},{
    "name": "block_list",
    "pos": {
        "left_top": (100, 50),
        "right_bottom": (300, -100)
    },
    "color": GRAY
}, {
    "name": "script",
    "pos": {
        "left_top": (300, 50),
        "right_bottom": (None, None)
    },
    "color": WHITE
}]



def get_screen_section_name(screen_section, screen_size, event_pos):
    event_x, event_y = event_pos

    for section in screen_section:
        section_name = section["name"]
        section_pos = section["pos"]
        x, y, w, h = unpack_section_position(section_pos, screen_size)
        if x <= event_x < x + w and y <= event_y < y + h:
            return section_name
    return None


def unpack_section_position(section_pos, screen_size):

    screen_width, screen_height = screen_size

    def coord_mapping(coord):
        x, y = coord
        if x == None:
            x = screen_width
        elif x < 0:
            x += screen_width
        if y == None:
            y = screen_height
        elif y < 0:
            y += screen_height
        return x, y
    
    start, end = section_pos["left_top"], section_pos["right_bottom"]

    x1, y1 = coord_mapping(start)
    x2, y2 = coord_mapping(end)
    w, h = x2-x1, y2-y1

    return (x1, y1, w, h)


def draw_screen_body(screen, screen_section):

    screen_size = get_current_screen_size(screen)

    for section in screen_section:
        section_name = section["name"]
        section_pos = section["pos"]
        color = section["color"]

        size = unpack_section_position(section_pos, screen_size)

        body = pygame.Rect(size)
        pygame.draw.rect(screen, color, body)






# 게임 루프
게임_실행중 = True
while 게임_실행중:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            게임_실행중 = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            screen_size = get_current_screen_size(screen)
            handle_click(event, screen_size)
        if event.type == pygame.MOUSEMOTION:
            handle_drag(event.pos)
        if event.type == pygame.MOUSEBUTTONUP:
            screen_size = get_current_screen_size(screen)
            handle_release(event, screen_size)

    # 현재 창 크기 텍스트 생성
    현재_크기_텍스트 = 폰트.render(f"현재 크기: {screen.get_width()} x {screen.get_height()}", True, BLACK)

    # 화면을 흰색으로 채우기
    screen.fill(WHITE)

    draw_screen_body(screen, screen_section)
    body = pygame.Rect(110, 60, 100, 50)
    pygame.draw.rect(screen, WHITE, body)
    draw_blocks()
    draw_coding_blocks()

    # 현재 창 크기 텍스트 표시
    screen.blit(현재_크기_텍스트, (10, 10))

    # 화면 업데이트
    pygame.display.flip()

# Pygame 종료
pygame.quit()
