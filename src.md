<h1 align="center">컴퓨터 물리 해석 1차 보고서</h1>
<p align="right">1202 김도윤 </p>
## 1. 물리적 유도

| 물리량                 | 기호         |
| ------------------- | ---------- |
| 받침대의 위치             | $X$        |
| 각 진자의 각도            | $\theta_i$ |
| 진자의 길이              | $r$        |
| 진자의 질량              | $m$        |
| 받침대의 질량             | $M$        |
| 저항력 ($\propto$ 각속도) | $b$        |
| 기타 받침대가 진자에게 주는 힘   | $F_i$      |
각 진자 끝의 속도는
$$
(\dot X + r \dot \theta_i \cos \theta_i, - r \dot \theta_i \cos \theta_i)
$$
로 나타내지며, 이의 진폭은
$$
\dot{X}^2 + 2r\cos{\theta_i}\dot{X}\dot{\theta_i} + r^2\dot{\theta_i}^2
$$
이다.
따라서 전체 운동에너지는
$$
T = 
\sum_{i=1}^n
\frac12 m(\dot{X}^2 + 2r\cos{\theta_i}\dot{X}\dot{\theta_i} + r^2\dot{\theta_i}^2)
+ \frac12M\dot{X}^2
$$
라는 것을 알 수 있다.
또한, 전체 포텐셜 에너지는
$$
V = - \sum_{i=1}^n mgr\cos{\theta_i}
$$
이다.

이때 라그랑지안을 보면:
$$
L = \sum_{i=1}^n \frac12 m {\dot X}^2
+ \sum_{i=1}^n mr\cos {\theta_i} \dot X \dot \theta_i
+ \sum_{i=1}^n \frac12mr^2 {\dot \theta_i}^2
+ \sum_{i=1}^n mgr\cos{\theta_i}
+ \frac12 M {\dot X}^2
$$
$$
\begin{align}
&\frac{\delta L}{\delta \dot \theta_i} =
mr \cos{\theta_i} \dot{X} + mr^2 \dot {\theta_i} \\

&\frac{d}{dt} \frac{\delta L}{\delta \dot \theta_i} =
mr \left(-\sin \theta_i \dot {\theta_i}\right)\dot{X} + mr \cos{\theta_i} \ddot X + mr^2 \ddot \theta_i \\

&\frac{\delta L}{\delta \theta_i} = mr (- \sin \theta_i) \dot X \dot \theta_i + mgr (- \sin \theta_i) \\

&\therefore mr\cos\theta_i \ddot X + m r^2 \ddot \theta_i = -mgr \sin \theta_i, \\
&\quad mr \ddot \theta_i = -mg \sin \theta_i - m \cos \theta_i \ddot X \tag{1}\\

&\frac{\delta L}{\delta \dot X} = (nm + M) \dot X + mr\sum_{i=1}^n \cos \theta_i \dot \theta_i \\

&\frac{d}{dt} \frac{\delta L}{\delta \dot X} = (nm + M) \ddot X + mr \sum_{i=1}^n (-sin \theta_i \dot \theta_i)\dot \theta_i + mr \sum_{i=1}^n \cos \theta_i \ddot \theta_i \\

&\frac{\delta L}{\delta X} = 0 \\

&\therefore (nm + M) \ddot X + mr \sum_{i=1}^n (-sin \theta_i \dot \theta_i)\dot \theta_i + mr \sum_{i=1}^n \cos \theta_i \ddot \theta_i = 0 \tag{2}
\end{align}
$$
저항력 $b \dot \theta_i$, 추가 힘 $F_i \cos \theta_i$를 추가하면:
$$
\begin{align}
&mr \ddot \theta_i = -mg \sin \theta_i - m \cos \theta_i \ddot X - bmr \dot \theta_i + F_i \cos \theta_i \tag{1'} \\

&mr \cos \theta_i \ddot \theta_i = -mg \sin \theta_i \cos \theta_i - m \cos^2 \theta_i \ddot X - bmr \cos \theta_i \dot \theta_i + F_i \cos^2 \theta_i\\
\end{align}
$$
이를 $(2)$에 대입하면:
$$
\begin{align}
(nm + M) \ddot X 
&- mr \sum_{i=1}^n \sin \theta_i {\dot \theta_i}^2 \\
&- mg \sum_{i=1}^n \sin \theta_i \cos \theta_i \\
&- m \ddot X \sum_{i=1}^n \cos^2 \theta_i \\
&- \sum_{i=1}^n bmr \cos \theta_i \dot \theta_i \\
&+ \sum_{i=1}^n F_i \cos^2 \theta_i = 0
\end{align}
$$
따라서:
$$
\ddot X = \frac{
\displaystyle
mr \sum_{i=1}^n \sin \theta_i {\dot \theta_i}^2 + mg \sum_{i=1}^n \sin \theta_i \cos \theta_i + \sum_{i=1}^n bmr \cos \theta_i \dot \theta_i - \sum_{i=1}^n F_i \cos^2 \theta_i
}{
\displaystyle
(nm+M) - m\sum_{i=1}^n \cos^2 \theta_i
}
$$
또한 $(1')$에서,
$$
\ddot \theta_i = \frac{-mg \sin \theta_i - m \cos \theta_i \ddot X - bmr \dot \theta_i + F_i \cos \theta_i}{mr}
$$
이는 이와 같이 구현한다:
```embed-python
PATH: vault://대전과학고 2-1/컴퓨터 물리 해석/spontaneous_synchronization/Simulation.py
TITLE: " "
LINES: "50-66"
```
## 2. 구현
$$
\vec X = [x_1, x_2, \cdots x_n, X]
$$
와 같이 변수들을 묶어주는 Data 클래스를 구현하고, 이에 대해 `__add__`, `__mul__` 등의 사칙연산을 구현해 하나의 값으로 다룰 수 있도록 하였다.

시뮬레이션의 state를 관리하는 Simulation 클래스와 이를 `vpython`으로 시각화하는 Visualizer 클래스를 만듦으로서 둘의 코드를 분리했고, 간단히 새로운 클래스를 생성하는 방법으로 매개변수가 다른 새로운 시뮬레이션을 만들 수 있도록 하였다.


진자에게 초기 충격량을 줄 수 있는 버튼과 시뮬레이션 속도를 바꿀 수 있는 슬라이더를 추가해 코드를 만지지 않고 활용할 수 있도록 하였고, 매개변수 섹션과 \<Restart\> 버튼을 따로 만들어 시뮬레이션의 여러 개의 요소를 바꿔가면서 실행할 수 있도록 하였다.

x-t 그래프와 최대 진폭, 그리고 위상 ($= \arctan2(x, v)$) 그래프를 제공함으로서 시뮬레이션의 양상을 확인할 수 있도록 하였다.
## 3. 결과
시간이 지날수록 진자의 위상이 모두 같아지는 것을 관찰할 수 있었다.

진자의 개수를 2개로 줄이고 진자의 진폭에 주목했는데, 여러 가지의 현상을 관찰할 수 있었다.
![](2025-04-29-095943.png)
(M = 100일 때의 진자의 진폭 양상)
![[2025-04-29-100127.png]]
(M = 10일 때의 진자의 진폭 양상)

진폭은 어떤 점에 대해서 감쇠진동하는 양상을 보였고, 이 양상의 주기를 구해 보았다.

- 일단 `amplitudes.py`에 최대진폭을 기록하는 함수를 구현했다.
- M이 20과 300 사이일 때의 (시간, 최대진폭)을 .csv 파일로 저장하는 `record_amplitudes.py`를 작성하였다.
- 두 진자의 진폭이 서로 교차하는 지점을 구하고, 이에 대해 선형 회귀해 주기를 구하는 `record_intersections.py`를 작성하였다.

![[2025-04-29-101018.png]]
(b = 0.01일 때의 진자의 진폭 양상)

이상하죠??