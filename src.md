<h1 align="center">컴퓨터 물리 해석 1차 보고서</h1>
<p align="right">1202 김도윤 </p>
## 1. 물리적 유도

| 물리량                 | 기호         | 기본값 |
| ------------------- | ---------- | --- |
| 받침대의 위치             | $X$        |     |
| 각 진자의 각도            | $\theta_i$ |     |
| 진자의 길이              | $r$        | 1   |
| 진자의 질량              | $m$        | 1   |
| 받침대의 질량             | $M$        | 100 |
| 저항력 ($\propto$ 각속도) | $b$        | 0.1 |
| 기타 받침대가 진자에게 주는 힘   | $F_i$      |     |
각 진자 끝의 속도는
$$
(\dot X + r \dot \theta_i \cos \theta_i, - r \dot \theta_i \cos \theta_i)
$$
로 나타내지며, 이의 속도$^2$은
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
 
운동량 보존, (b = 0일때) 에너지 보존 등으로 위 구현의 정확성을 확인할 수 있었다.

메트로놈은 단진자 뿐만 아니라 중심을 지날 때마다 진자에게 추가적인 힘을 주는 태엽 장치가 있다. 이 시뮬레이션에선 중심에서 멀어지는 쪽으로 `angle_threshold`(기본값 0.1)를 넘었을 때 `impulse`(기본값 0.1)의 충격량을 주는 방법으로 이를 구현했다:
## 2. 구현
$$
\vec X = [x_1, x_2, \cdots x_n, X]
$$
와 같이 변수들을 묶어주는 Data 클래스를 구현하고, 이에 대해 `__add__`, `__mul__` 등의 사칙연산을 구현해 하나의 값으로 다룰 수 있도록 하였다.

시뮬레이션의 state를 관리하는 Simulation 클래스와 이를 `vpython`으로 시각화하는 Visualizer 클래스를 만듦으로서 둘의 코드를 분리했고, 새로운 클래스를 생성하는 방법으로 매개변수가 다른 새로운 시뮬레이션을 간단히 만들 수 있도록 하였다.


진자에게 초기 충격량을 줄 수 있는 버튼과 시뮬레이션 속도를 바꿀 수 있는 슬라이더를 추가해 코드를 만지지 않고 활용할 수 있도록 하였고, 매개변수 섹션과 \<Restart\> 버튼을 따로 만들어 시뮬레이션의 여러 개의 요소를 바꿔가면서 실행할 수 있도록 하였다.

x-t 그래프와 최대 진폭, 그리고 위상 ($= \arctan2(x, v)$) 그래프를 제공함으로서 시뮬레이션의 양상을 확인할 수 있도록 하였다.

## 3. AI 활용
1차 시도에는 AI를 중심으로 코드 작성을 시도하였으나, 관리가 어려워져 폐기하였다. 초반에는 AI에게 `vpython` 예시를 부탁해 새로운 라이브러리를 익힐 수 있었다. 다만 이후에는 직접 문서를 찾아보며 개발을 진행했다.

위의 라그랑지안 계산 중 외부 힘을 더하는 과정에서 운동량 보존이 정확히 되지 않는 점을 발견했는데, AI와 상호 교섭한 결과 틀린 항을 발견할 수 있었다.
## 4. 결과
시간이 지날수록 진자의 위상이 모두 같아지는 것을 관찰할 수 있었다. 정성적으로 관찰한 바로는:
- b가 클수록, M이 작을수록 위상 동기화가 더 빠르게 되었다.
- 모두 같은 위상으로 진동하는 경우만 관찰할 수 있었고, 위상이 $\pi$만큼 다른 상태로 진동하는 경우는 일시적으로 존재하긴 했지만 불안정해 모두 같은 위상으로 돌아갔다.
- 주기는 $\sqrt{r}$에 대략적으로 반비례했다.
### (1) M에 따른 진자의 진폭 양상
진자의 개수를 2개로 줄이고 진자의 진폭에 주목했는데, 여러 가지의 현상을 관찰할 수 있었다.
![](2025-04-29-095943.png)

(M = 100일 때의 진자의 진폭 양상)
![[2025-04-29-100127.png]]

(M = 10일 때의 진자의 진폭 양상)

진폭은 어떤 점에 대해서 감쇠진동하는 양상을 보였고, 이 양상의 주기를 구해 보았다.

- 일단 `amplitudes.py`에 최대진폭을 기록하는 함수를 구현했다.
- M이 20과 300 사이일 때의 (시간, 최대진폭)을 `output/{M}.csv` 파일로 저장하는 `record_amplitudes.py`를 작성하였다.
- 두 진자의 진폭이 서로 교차하는 지점을 구하고, 이에 대해 선형 회귀해 주기를 구하는 `record_intersections.py`를 작성하였다. `periods.csv`에서 이를 볼 수 있다.

결과값들은 다음과 같다:
![[graph.png]]
추세선 분석 결과, 비례한다고 가정했을 때와 제곱근과 비례한다고 가정했을 때 둘 다 0.98 정도의 $R^2$값이 나왔고, Power함수로 가정했을 때:
![[graph0.65.png]]
이와 같은 결과가 나왔다. 다만 지수값 0.65에 대해서는 추후 탐구가 필요할 듯 하다.
### (2) b (저항값)에  따른 진자의 진폭 양상
b는 진자의 움직임을 받침대에 전달하는 역할을 하므로, b가 작으면 동기화하는 시간도 느려지는 것을 확인할 수 있었다.

![[2025-04-29-101018.png]]

(b = 0.01일 때의 진자의 진폭 양상)

저항값이 작은 경우에는 위와 같이 진폭 차이가 줄어드는 구간도 있고 커지는 구간도 있는데, 위상 그래프와 대조해서 보면 이것은 위상 차이가 $\pi$보다 큰 상황에서 에너지가 반대로 전달되는 경우인 것을 확인할 수 있다.
### (3) 진자의 고유 진동수가 다른 경우의 진자의 진폭 및 위상 양상
진자 4개의 길이는 1, 1개의 길이는 0.9인 상태로 시뮬레이션을 실행했다.
![[diff_amp.png]]

(빨강: 0.9)

이와 같이 길이가 짧은 (주기가 짧은) 의 위상이 약간 앞서고, 진폭이 더 큰 것을 관찰할 수 있었다.

1개의 길이를 0.8로 더 줄이면:
![[x0.8.png]]
이와 같이 더 이상 동기화 되지 않으며,
![[amp0.8.png]]
이와 같이 위상 차이가 변동하면서 각 진자의 진폭도 같이 변동하는 것을 관찰할 수 있었다. 이분탐색으로 반복 실험한 결과 이 임계값은 0.8625와 0.875 사이임을 알 수 있었다.
## 5. 보완할 점
각 진자가 받침대에 어느 정도의 힘을 가하고 있고, 이들이 다른 진자의 움직임을 돕는지 반하는지에 대해 시각화 및 분석을 할 계획이었지만, 시간이 부족해 할 수 없었다.
각 진자의 길이 (즉, 고유 진동수)가 다른 경우에 대해서도 시뮬레이션을 하였지만, 이를 GUI를 사용하여 조절할 수 있게 하진 못했다.
또한, 각 진자의 길이가 다른 경우에는 $b$와 $M$과 같은 다른 변수에 의해서도 임계값이 달라지는데, 이를 자동으로 측정하기 위해선 동기화했는지에 대한 판단 기준이 필요하며, 훨씬 성능이 좋은 시뮬레이션이 필요하기 때문에 하지 못했다.
## 6. 부록: 각 진자의 길이가 다른 경우의 물리적 유도
$$
\begin{align}
&T = 
\sum_{i=1}^n
\frac12 m(\dot{X}^2 + 2r_i\cos{\theta_i}\dot{X}\dot{\theta_i} + r_i^2\dot{\theta_i}^2)
+ \frac12M\dot{X}^2 \\
&V = - \sum_{i=1}^n mgr_i\cos{\theta_i} \\
&L = \sum_{i=1}^n \frac12 m {\dot X}^2
+ \sum_{i=1}^n mr_i\cos {\theta_i} \dot X \dot \theta_i
+ \sum_{i=1}^n \frac12mr_i^2 {\dot \theta_i}^2
+ \sum_{i=1}^n mgr_i\cos{\theta_i}
+ \frac12 M {\dot X}^2 \\

&\frac{\delta L}{\delta \dot \theta_i} =
mr_i \cos{\theta_i} \dot{X} + mr_i^2 \dot {\theta_i} \\

&\frac{d}{dt} \frac{\delta L}{\delta \dot \theta_i} =
mr_i \left(-\sin \theta_i \dot {\theta_i}\right)\dot{X} + mr_i \cos{\theta_i} \ddot X + mr_i^2 \ddot \theta_i \\

&\frac{\delta L}{\delta \theta_i} = mr_i (- \sin \theta_i) \dot X \dot \theta_i + mgr_i (- \sin \theta_i) \\

&\therefore mr_i\cos\theta_i \ddot X + m r_i^2 \ddot \theta_i = -mgr_i \sin \theta_i, \\
&\quad mr_i \ddot \theta_i = -mg \sin \theta_i - m \cos \theta_i \ddot X \tag{1}\\

&\frac{\delta L}{\delta \dot X} = (nm + M) \dot X + m\sum_{i=1}^n r_i\cos \theta_i \dot \theta_i \\

&\frac{d}{dt} \frac{\delta L}{\delta \dot X} = (nm + M) \ddot X + m \sum_{i=1}^n r_i(-sin \theta_i \dot \theta_i)\dot \theta_i + m \sum_{i=1}^n r_i \cos \theta_i \ddot \theta_i \\

&\frac{\delta L}{\delta X} = 0 \\

&\therefore (nm + M) \ddot X + m \sum_{i=1}^n r_i(-sin \theta_i \dot \theta_i)\dot \theta_i + m \sum_{i=1}^n r_i\cos \theta_i \ddot \theta_i = 0 \tag{2} \\

&mr_i \ddot \theta_i = -mg \sin \theta_i - m \cos \theta_i \ddot X - bmr_i \dot \theta_i + F_i \cos \theta_i \tag{1'} \\

&mr_i \cos \theta_i \ddot \theta_i = -mg \sin \theta_i \cos \theta_i - m \cos^2 \theta_i \ddot X - bmr_i \cos \theta_i \dot \theta_i + F_i \cos^2 \theta_i\\

&(nm + M) \ddot X 
- m \sum_{i=1}^n r_i\sin \theta_i {\dot \theta_i}^2 
- mg \sum_{i=1}^n \sin \theta_i \cos \theta_i 
- m \ddot X \sum_{i=1}^n \cos^2 \theta_i 
- \sum_{i=1}^n bmr_i \cos \theta_i \dot \theta_i 
+ \sum_{i=1}^n F_i \cos^2 \theta_i = 0 \\

&\ddot X = \frac{
\displaystyle
m \sum_{i=1}^n r_i\sin \theta_i {\dot \theta_i}^2 + mg \sum_{i=1}^n \sin \theta_i \cos \theta_i + \sum_{i=1}^n bmr_i \cos \theta_i \dot \theta_i - \sum_{i=1}^n F_i \cos^2 \theta_i
}{
\displaystyle
(nm+M) - m\sum_{i=1}^n \cos^2 \theta_i
}

\end{align}
$$

