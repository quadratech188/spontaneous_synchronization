from Simulation import Simulation
from Visualizer import Visualizer
import pygame
from vpython import *
import numpy as np
import math

fps = 100
dt = 1 / fps

n = 5
m = 1
M = 100
r = 1
b = 0.1
angle_threshold = 0.1
impulse = 0.1

initial_impulse = 2
timescale = 1

pygame.init()
pygame.mixer.init()

click = pygame.mixer.Sound('click.wav')

while True:
    scene.delete()
    scene = canvas()

    simulation = Simulation(
            n,
            m,
            M,
            r,
            b,
            angle_threshold,
            impulse
            )

    def play_click(index, dir):
        click.play()

    # simulation.add_escapement_hook(play_click)

    visualizer = Visualizer(simulation)

    angle_graph = graph(title='x - t', xtitle='t(s)', ytitle='x(rad)', xmin=-5, xmax=0, scroll=True)

    angle_curves = [gcurve(color=color.hsv_to_rgb(vector(i / n, 1, 1))) for i in range(n)]
    for curve in angle_curves:
        curve.plot(0, 0)

    scene.title = '<h1>Spontaneous Synchronization</h1>'
    timescale_text = wtext(text=f'Time Factor: {timescale}x\n')

    def timescale_slider_callback(evt):
        global timescale
        timescale = int(evt.value)
        timescale_text.text = f'Time Factor: {timescale}x\n'

    timescale_slider = slider(bind=timescale_slider_callback, min=1, max=10, step=1, value=timescale)
    scene.append_to_caption('\n\n')

    initial_impulse_text = wtext(text=f'Initial Impulse: {initial_impulse}\n')
    def initial_amplitude_callback(evt):
        global initial_impulse
        initial_impulse = evt.value
        initial_impulse_text.text = f'Initial Impulse: {initial_impulse}\n'

    initial_impulse_slider = slider(bind=initial_amplitude_callback, min=0, max=5, value=initial_impulse)
    scene.append_to_caption('\n\n')

    def left_callback(evt):
        simulation.forces[evt.id] -= initial_impulse / dt

    def right_callback(evt):
        simulation.forces[evt.id] += initial_impulse / dt

    for i in range(n):
        button(text='<', bind=left_callback, id=i)
        scene.append_to_caption(f' {i} ')
        button(text='>', bind=right_callback, id=i)
        scene.append_to_caption(f'    ')

    scene.append_to_caption('\n')

    settings = [n, m, M, r, b, angle_threshold, impulse]

    scene.append_to_caption('<h2>Config</h2>')

    # 일반적으로 할 수 있는 만족스러운 방법을 찾지 못해 결국 코드 중복을 받아들이기로 했다.
    def n_callback(evt):
        global n
        n = evt.number
    scene.append_to_caption('\nn\n')
    winput(bind=n_callback, text=str(n))

    def m_callback(evt):
        global m
        m = evt.number
    scene.append_to_caption('\nm\n')
    winput(bind=m_callback, text=str(m))

    def M_callback(evt):
        global M
        M = evt.number
    scene.append_to_caption('\nM\n')
    winput(bind=M_callback, text=str(M))

    def r_callback(evt):
        global r
        r = evt.number
    scene.append_to_caption('\nr\n')
    winput(bind=r_callback, text=str(r))

    def b_callback(evt):
        global b
        b = evt.number
    scene.append_to_caption('\nb\n')
    winput(bind=b_callback, text=str(b))

    def angle_threshold_callback(evt):
        global angle_threshold
        angle_threshold = evt.number
    scene.append_to_caption('\nAngle Threshold\n')
    winput(bind=angle_threshold_callback, text=str(angle_threshold))

    def impulse_callback(evt):
        global impulse
        impulse = evt.number
    scene.append_to_caption('\nImpulse\n')
    winput(bind=impulse_callback, text=str(impulse))

    stop = False

    def restart():
        global stop
        stop = True

    button(bind=restart, text='Restart')

    maximums = [(0.0, 0.0) for _ in range(n)]
    maximums_graph = graph(title='Maximum Amplitudes (x - t)', xtitle='t(s)', ytitle='x(rad)', xmin=-200, xmax=0, scroll=True)
    maximums_curves = [gcurve(color=color.hsv_to_rgb(vector(i / n, 1, 1))) for i in range(n)]
    for curve in maximums_curves:
        curve.plot(0, 0)


    def update_maximums(i, dir):
        maximums_curves[i].plot(*maximums[i])
        maximums[i] = (0.0, 0.0)

    simulation.add_escapement_hook(update_maximums)

    phase_graph = graph(title = 'Phase(theta - t)', xtitle='t(s)', ytitle='theta(rad)', xmin=-5, xmax=0, scroll=True)
    phase_curves = [gcurve(color=color.hsv_to_rgb(vector(i / n, 1, 1))) for i in range(n)]
    for curve in phase_curves:
        curve.plot(0, 0)

    t = 0
    while not stop:
        rate(fps)

        # timescale (배속 정도)에 따라 시뮬레이션을 더 많이 돌린다.
        for i in range(timescale):
            simulation.step(dt)

            for i in range(simulation.n):
                # 최대 진폭 업데이트
                if (maximums[i][1] < abs(simulation.x.x[i])):
                    maximums[i] = (t, abs(simulation.x.x[i]))

            t += dt

        visualizer.update()

        for i in range(simulation.n):
            angle_curves[i].plot(t, simulation.x.x[i])
            phase_curves[i].plot(t, math.atan2(simulation.x.x[i], simulation.v.x[i]))

    # 모든 것 리셋. Restart 버튼 클릭 후 모두 지운 후, 새로 만드는 방법으로 config 업데이트를 반영한다.
    angle_graph.delete()
    maximums_graph.delete()
    phase_graph.delete()

    scene.caption = ''
    scene.title = ''
