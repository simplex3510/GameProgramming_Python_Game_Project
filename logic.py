import random
import contents as c

TOTAL_SCORE = 0

#####################
# 게임 플로우 관련 함수 #
#####################

# 새 게임 시작, n=4로 전달받음
def new_game(n):
    # 매트릭스 생성
    matrix = []
    # 4번 반복 -> 4*4 매트릭스 설정
    for i in range(n):
        # 매트릭스 리스트에 [-1],[-1],[-1],[-1] 추가
        matrix.append([-1] * n)
    # 매트릭스 리스트 반환
    return matrix

# 게임 상태 판단
def game_state(mat):

    for i in range(len(mat)):               # 4번 반복 - 열의 증가
        for j in range(len(mat[0])):        # 해당 행의 개수만큼 반복
            if mat[i][j] == 1:           # 1 타일의 존재 검사
                return 'win'

    for i in range(len(mat)-1):             # 0, 1, 2열 검사
        for j in range(len(mat[0])-1):      # 0, 1, 2행 검사
            # 인접한 타일(아래쪽, 오른쪽) 2개의 값이 서로 같은 것이 있는가?
            if mat[i][j] == mat[i+1][j] or mat[i][j] == mat[i][j+1]:
                return 'not over'

    # 가장 오른쪽 하단의 타일 검사
    if mat[len(mat)-1][len(mat)-1] == mat[2][3]:
        return 'not over'
    elif mat[len(mat)-1][len(mat)-1] == mat[3][2]:
        return 'not over'

    for i in range(len(mat)):               # 4번 반복 - 열의 증가
        for j in range(len(mat[0])):        # 해당 행의 개수만큼 반복
            if mat[i][j] == -1:              # 빈 타일의 존재 검사
                return 'not over'

    for k in range(len(mat)-1):             # 0, 1, 2행 검사
        # 인접한 좌우 타일의 값이 동인한지 검사
        if mat[len(mat)-1][k] == mat[len(mat)-1][k+1]:
            return 'not over'

    for j in range(len(mat)-1):             # 0, 1, 2열 검사
        # 인접한 상하 타일의 값이 동일한지 검사
        if mat[j][len(mat)-1] == mat[j+1][len(mat)-1]:
            return 'not over'

    return 'lose'                           # 그 외의 경우에는 패배

################
# 타일 관련 함수 #
################

# 새로운 타일 생성
def create_tile(mat):
    # 임의의 좌표를 각각의 변수에 저장
    a = random.randint(0, len(mat)-1)
    b = random.randint(0, len(mat)-1)
    # 해당 좌표의 값이 0일 경우 (비어있을 경우)
    while(mat[a][b] != -1):
        a = random.randint(0, len(mat)-1)
        b = random.randint(0, len(mat)-1)
    # 해당 좌표의 값을 2로 설정(새로운 타일 생성)
    mat[a][b] = 2048
    return mat

# 타일 변경
def change_tile(mat):
    # 0 ~ 9까지의 임의의 정수 받아옴
    do = (random.randint(0, 9))
    # 1/10의 확률로 5가 걸리면
    if do == 5:
        # 임의의 좌표값을 설정함
        index = (random.randint(0, 3), random.randint(0, 3))
        # 비어있을 때까지 반복
        while mat[index[0]][index[1]] == 0:
            index = (random.randint(0, 3), random.randint(0, 3))
        # 해당 타일의 값을 2의 2승(4) ~ 11승(2048) 중의 하나로 변경
        mat[index[0]][index[1]] = 2 ** random.randint(2, 11)
    return mat

# 타일 소멸
def disappear_tile(mat, x, y):
    do = (random.randint(0, 6))
    if do == 3:
        mat[x][y] = -1
    return mat

#################
# 게임 메인 시스템 #
#################

# 90도 회전
def degree_90(mat):
    new = []                             # 새로운 리스트 생성
    for i in range(4):         # 4번 반복 - 해당 가로열의 요소 개수
        new.append([])                   # 4개의 리스트 추가 (2차원 리스트)
        for j in range(3, -1, -1):        # 4번 반복
            new[i].append(mat[j][i])     # 세로로 정렬
    # 세로로 정렬된 리스트 반환
    return new

# 왼쪽 정렬 함수
def cover_up(mat):
    new = []                                # new 리스트 생성 - 왼쪽으로 정렬된 값을 입력받음
    for i in range(c.GRID_LEN):             # 4번 반복
        partial_new = []                    # 부분적 new 리스트 생성
        for j in range(c.GRID_LEN):         # 4번 반복
            partial_new.append(-1)          # 부분적 new 리스트에 0 추가
        new.append(partial_new)             # new 리스트에 [0, 0, 0, 0] 추가 - partial_new
    done = False                            # done을 False로 전환

    for i in range(c.GRID_LEN):             # 4번 반복
        count = 0                           # 카운트 생성 - 왼쪽으로부터 몇 번째에 저장될지 명시
        for j in range(c.GRID_LEN):         # 4번 반복
            if mat[i][j] != -1:              # 해당 매트릭스 좌표의 값이 0이 아니면 - 빈 타일은 무시
                new[i][count] = mat[i][j]   # mat 리스트의 값을 new 리스트에 왼쪽으로 정렬하여 저장
                if j != count:              # j가 count와 같지 않다면
                    done = True             # done을 True로 전환
                count += 1                  # 다음 인덱스에 저장해야 하므로 1증가

    # new 리스트와 done의 상태를 반환
    return (new, done)

# 타일 합병 함수 및 점수 증가
def merge(mat):
    global TOTAL_SCORE
    done = False                            # done을 False로 전환
    for i in range(c.GRID_LEN):             # 4번 반복
        for j in range(c.GRID_LEN-1):       # 0, 1, 2번째까지만 접근
            # 해당 좌표와 인접한 오른쪽 값이 같음 + 둘 다 0이 아닐 경우
            # 즉, 0이 아닌 타일 2개가 서로 같은가
            if mat[i][j] == mat[i][j+1] and mat[i][j] != -1:
                mat[i][j] = int(mat[i][j] / 2)              # 해당 좌표값 1/2배 - 다음 레벨 타일
                mat[i][j+1] = -1                            # 오른쪽 값은 소멸 - 피합병 타일 소멸
                TOTAL_SCORE += mat[i][j]                    # 생성된 값만큼 점수 증가
                #mat = disappear_tile(mat, i, j)
                done = True                 # done을 True로 전환

    # 변화된 매트릭스 리스트와 done 상태를 반환
    return (mat, done, TOTAL_SCORE)

#####################
# 입력된(키) 명령 실행 #
#####################

def up(game):
    print("up")
    game = degree_90(game); game = degree_90(game); game = degree_90(game)
    game, done = cover_up(game)
    temp = merge(game)                  # temp에 merge 이후의 game을 저장
    done = done or temp[1]
    game = cover_up(game)[0]
    game = degree_90(game)
    return (game, done, TOTAL_SCORE)

def down(game):
    print("down")
    game = degree_90(game)     #
    game, done = cover_up(game)
    temp = merge(game)                  # temp에 merge 이후의 game을 저장
    done = done or temp[1]
    game = cover_up(game)[0]
    game = degree_90(game); game = degree_90(game); game = degree_90(game)
    return (game, done, TOTAL_SCORE)

def left(game):
    print("left")
    game, done = cover_up(game)
    temp = merge(game)                  # temp에 merge 이후의 game을 저장
    done = done or temp[1]
    game = cover_up(game)[0]
    return (game, done, TOTAL_SCORE)

def right(game):
    print("right")
    game = degree_90(game); game = degree_90(game)
    game, done = cover_up(game)
    temp = merge(game)                  # temp에 merge 이후의 game을 저장
    done = done or temp[1]
    game = cover_up(game)[0]
    game = degree_90(game); game = degree_90(game)
    return (game, done, TOTAL_SCORE)
