# GUI 모듈을 포함시킴
from tkinter import Frame, Label, CENTER

import logic
import contents as c

TOTAL_SCORE = 0

class GameGrid(Frame):
    # 초기화 함수
    def __init__(self):
        # 프레임 생성
        Frame.__init__(self)

        self.grid()                                     # 그리드 설정
        self.master.title('2048?')                      # 윈도우 창 이름 설정
        self.master.bind("<Key>", self.key_down)        # 키 입력, 어떤 함수를 키에 종속(bind)

        # self.gamelogic = gamelogic
        # 입력 키 커맨드 정의
        self.commands = {c.KEY_UP: logic.up,        c.KEY_UP_ALT: logic.up,         c.KEY_K: logic.up,
                         c.KEY_DOWN: logic.down,    c.KEY_DOWN_ALT: logic.down,     c.KEY_J: logic.down,
                         c.KEY_LEFT: logic.left,    c.KEY_LEFT_ALT: logic.left,     c.KEY_H: logic.left,
                         c.KEY_RIGHT: logic.right,  c.KEY_RIGHT_ALT: logic.right,   c.KEY_L: logic.right}

        # 종합 점수
        self.total_score = []
        # 그리드 셀즈 리스트
        self.grid_fields = []
        # 스코어 그리드 초기화
        self.init_grid_score()
        # 그리드 초기화
        self.init_grid()
        # 매트릭스 초기화
        self.init_matrix()
        # 그리드 셀즈 업데이트
        self.update_grid()
        # 윈도우 창을 윈도우가 종료될 때까지 실행시킴
        self.mainloop()

    # 스코어 그리드 초기화
    def init_grid_score(self):
        # 아웃사이드 배경 프레임 생성
        # 프레임(셀프 윈도우, 배경 색상, 배경 너비, 배경 높이)
        background_out = Frame(self, bg=c.BACKGROUND_COLOR_GAME, width=c.SIZE, height=c.SIZE)
        background_out.grid()  # 배경 그리드 생성, 윈도우 창에 배치

        # 인사이드 배경 설정 및 그리드
        background_in = Frame(background_out, bg=c.BACKGROUND_COLOR_field_EMPTY, width= 676, height=200)
        background_in.grid(row=0, column=0, padx=c.GRID_PADDING, pady=c.GRID_PADDING)

        # 스코어 위젯 설정 및 그리드
        score = Label(background_in, text="score: " + str(self.total_score),
                      bg=c.BACKGROUND_COLOR_field_EMPTY, fg=c.GAME_STATE_TEXT,
                      justify=CENTER, font=c.FONT, width=18, height=2)
        score.grid()

        self.total_score.append(score)

    # 그리드 초기화
    def init_grid(self):
        # 배경 프레임 생성
        # 배경 화면 = 프레임(셀프 윈도우, 배경 색상, 배경 너비, 배경 높이)
        background = Frame(self, bg=c.BACKGROUND_COLOR_GAME, width=c.SIZE, height=c.SIZE)
        background.grid()   # 배경 그리드 생성, 윈도우 창에 배치

        # 각각의 셀에 프레임을 생성하고 그리드 설정
        for i in range(c.GRID_LEN):
            grid_row = []               # 4개의 가로 그리드 리스트 생성
            for j in range(c.GRID_LEN):

                # 셀 프레임(배경 윈도우, 셀 배경색, 셀 너비 = 100, 셀 높이 = 100)
                field = Frame(background, bg=c.BACKGROUND_COLOR_field_EMPTY,
                             width=c.SIZE / c.GRID_LEN,
                             height=c.SIZE / c.GRID_LEN)

                # 셀 그리드(가로 위치, 세로 위치, 위젯에 대한 x방향 외부 패딩, 위젯에 대한 y방향 외부 패딩)
                field.grid(row=i, column=j,
                          padx=c.GRID_PADDING,
                          pady=c.GRID_PADDING)

                # (가장 앞)master윈도우, 출력 문자열(비어있음), 타일 배경 색상, 화면 중앙 정렬, 폰트, 가로4, 세로2
                tile = Label(master = field, text="",
                          bg=c.BACKGROUND_COLOR_field_EMPTY,
                          justify=CENTER, font=c.FONT, width=4, height=2)

                # 타일 그리드
                tile.grid()

                # 가로 그리드 리스트에 설정한 타일 추가 - 4번 반복
                grid_row.append(tile)

            # 그리드 셀즈에 가로 그리드 추가 - 4번 반복
            self.grid_fields.append(grid_row)

    # 매트릭스 초기화
    def init_matrix(self):
        # 매트릭스 리스트 생성, 4를 전달
        self.matrix = logic.new_game(c.GRID_LEN)
        # 히스토리 매트릭스 리스트 생성, 비어있음
        self.history_matrixs = list()
        # 기본 시작 시의 2타일 2개 생성
        '''self.matrix[0][3] = 4
        self.matrix[2][3] = 4'''
        self.matrix = logic.create_tile(self.matrix)
        self.matrix = logic.create_tile(self.matrix)

    # 화면에 출력될 그리드 셀즈 업데이트
    def update_grid(self):

        # 매트릭스 전체 값을 검사
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN):
                # 뉴 넘버에 해당 좌표의 값을 저장
                new_number = self.matrix[i][j]
                if new_number == -1 or new_number == 1:             # 뉴 넘버가 -1 또는 1이라면(타일이 없다면)
                    # 그리드 셀즈에 있는 해당 좌표의 값을
                    # (텍스트 출력 안 함, 빈 배경 색상)으로 변경
                    self.grid_fields[i][j].configure(
                        text="", bg=c.BACKGROUND_COLOR_field_EMPTY)

                else:                           # 타일이 있다면
                    # 그리드 셀즈에 있는 해당 좌표의 값을
                    # (뉴 넘버 문자열 출력, 뉴 넘버에 대응하는 배경 색상, 뉴 넘버에 대응하는 문자 색상)
                    self.grid_fields[i][j].configure(text=str(new_number),
                        bg=c.BACKGROUND_COLOR_DICT[new_number],
                        fg=c.field_COLOR_DICT[new_number])

        self.total_score[0].configure(text= "score: " + str(TOTAL_SCORE))

        # 모두 검사 후, 화면 출력을 업데이트
        self.update_idletasks()

    # 키보드 입력 판단
    def key_down(self, event):
        # 변수에 키보드 이벤트에서 발생하는 문자를 문자열 객체로 저장
        key = repr(event.char)
        #print(repr(event.char))

        # 입력된 키가 'b' + 히스토리 매트릭스의 길이가 2이상일 경우
        if (key == c.KEY_BACK) and (len(self.history_matrixs) >= 1):
            # 저장된 이전 매트릭스를 불러옴
            self.matrix = self.history_matrixs.pop()
            # 화면 출력 업데이트
            self.update_grid()
            # 되돌리기 문구 출력: 남은 히스토리 매트릭스 길이(되돌릴 수 있는 회수)
            print('back on step total step:', len(self.history_matrixs))

        elif key in self.commands:
            global TOTAL_SCORE
            #                                      ex) logic.up(self.matrix)
            self.matrix, done, TOTAL_SCORE = self.commands[repr(event.char)](self.matrix)

            # done이 참이라면
            if done:
                # 히스토리 매트릭스 리스트에 직전 움직임 기록
                self.history_matrixs.append(self.matrix)
                # 타일 변경
                self.matrix = logic.change_tile(self.matrix)
                # 매트릭스에 새로운 타일 생성
                self.matrix = logic.create_tile(self.matrix)

                # 화면 출력 업데이트
                self.update_grid()
                # done을 Flase로 전환
                done = False

                #  게임에서 승리할 경우
                if logic.game_state(self.matrix) == 'win':
                    self.grid_fields[1][1].configure(
                        text="You", bg=c.BACKGROUND_COLOR_field_EMPTY, fg=c.GAME_STATE_TEXT)
                    self.grid_fields[1][2].configure(
                        text="Win!", bg=c.BACKGROUND_COLOR_field_EMPTY, fg=c.GAME_STATE_TEXT)

                # 게임에서 패배할 경우
                if logic.game_state(self.matrix) == 'lose':
                    self.grid_fields[1][1].configure(
                        text="You", bg=c.BACKGROUND_COLOR_field_EMPTY)
                    self.grid_fields[1][2].configure(
                        text="Lose!", bg=c.BACKGROUND_COLOR_field_EMPTY)

gamegrid = GameGrid()
