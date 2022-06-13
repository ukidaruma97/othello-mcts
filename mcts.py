from game import random_action
import math

#플레이아웃
def playout(state):
    # 패배 시, 상태 가치 -1
    if state.is_lose():
        return -1
    
    # 무승부 시, 상태 가치 0
    if state.is_draw():
        return  0
    
    # 다음 상태의 상태 평가
    return -playout(state.next(random_action(state)))

# 원시 몬테카를로 탐색을 활용한 행동 선택
def mcs_action(state):
    # 합법적인 수 별로 150회 플레이아웃 시행 후, 상태 가치의 합계 계산
    legal_actions = state.legal_actions()
    values = [0] * len(legal_actions)
    for i, action in enumerate(legal_actions):
        for _ in range(150):
            values[i] += -playout(state.next(action))

    # 합법적인 수의 상태 가치 합계의 최대값을 가지는 행동 반환
    return legal_actions[argmax(values)]

# 최대값의 인덱스를 반환
def argmax(collection, key=None):
    return collection.index(max(collection))

# 몬테카를로 트리 탐색의 행동 선택
def mcts_action(state):
    # 몬테카를로 트리 탐색의 노드 정의
    class Node:
        # 노드 초기화
        def __init__(self, state):
            self.state = state # 상태
            self.w = 0 # 보상 누계
            self.n = 0 # 시행 횟수
            self.child_nodes = None  # ㅈ녀 노드 군

        # 국면 가치 계산
        def evaluate(self):
            # 게임 종료 시
            if self.state.is_done():
                # 승패 결과로 가치 취득
                value = -1 if self.state.is_lose() else 0 # 패배 시 -1, 무승부 시 0

                # 보상 누계와 시행 횟수 갱신
                self.w += value
                self.n += 1
                return value

            # 자녀 노드가 존재하지 않는 경우
            if not self.child_nodes:
                # 플레이아웃으로 가치 얻기
                value = playout(self.state)

                # 보상 누계와 시행 횟수 갱신
                self.w += value
                self.n += 1

                # 자녀 노드 전개
                if self.n == 150: 
                    self.expand()
                return value

            # 자녀 노드가 존재하는 경우
            else:
                # UCB1이 가장 큰 자녀 노드를 평가해 가치 얻기
                value = -self.next_child_node().evaluate() 

                # 보상 누계와 시행 횟수 갱신
                self.w += value
                self.n += 1
                return value

        # 자녀 노드 전개
        def expand(self):
            legal_actions = self.state.legal_actions()
            self.child_nodes = []
            for action in legal_actions:
                self.child_nodes.append(Node(self.state.next(action)))

        # UCB1이 가장 큰 자녀 노드 얻기
        def next_child_node(self):
             # 시행 횟수가 0인 자녀 노드 반환
            for child_node in self.child_nodes:
                if child_node.n == 0:
                    return child_node

            # UCB1 계산
            t = 0
            for c in self.child_nodes:
                t += c.n
            ucb1_values = []
            for child_node in self.child_nodes:
                ucb1_values.append(-child_node.w/child_node.n+(2*math.log(t)/child_node.n)**0.5)

            # UCB1이 가장 큰 자녀 노드 반환
            return self.child_nodes[argmax(ucb1_values)]    
    
    # 현재 국면의 노드 생성
    root_node = Node(state)
    root_node.expand()

    # 100회 시뮬레이션 실행
    for _ in range(100):
        root_node.evaluate()

    # 시행 횟수가 가장 큰 값을 갖는 행동 반환
    legal_actions = state.legal_actions()
    n_list = []
    for c in root_node.child_nodes:
        n_list.append(c.n)
    return legal_actions[argmax(n_list)]
