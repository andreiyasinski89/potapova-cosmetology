#!/usr/bin/env python3
"""Робить із короткого відео hero (≈6 с) довгу безшовну петлю ≥10 с методом «туди й назад» (boomerang):
   вперед → назад. Останній кадр дорівнює першому, тому момент перезапуску не видно, а артефактів
   інтерполяції чи «двійників» при склейці немає.
Запуск: python tools/make-hero-loop.py <вихідне відео>   (результат: assets/video/hero-loop.mp4)"""
import os, subprocess, sys

src = sys.argv[1]
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'video', 'hero-loop.mp4')
fc = '[0:v]scale=1080:-2,split[a][b];[b]reverse[r];[a][r]concat=n=2:v=1:a=0[out]'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-filter_complex', fc, '-map', '[out]', '-an',
                '-c:v', 'libx264', '-crf', '29', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], check=True)
d = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=nw=1:nk=1', out], capture_output=True, text=True).stdout.strip()
print(f'петля {float(d):.2f} с, {os.path.getsize(out)/1e6:.2f} МБ: {out}')
