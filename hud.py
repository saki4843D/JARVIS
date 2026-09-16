from __future__ import annotations

import math
import threading
import time
from typing import Optional

import pygame
import psutil

FPS = 30
BLACK = (4, 8, 16)
BG = (7, 15, 24)
BLUE = (67, 194, 255)
CYAN = (156, 220, 255)
GREEN = (121, 255, 167)
ORANGE = (255, 154, 71)
RED = (255, 94, 104)
WHITE = (236, 244, 255)
GRAY = (101, 118, 140)


class JarvisHUD:
    """Desktop HUD for laptop telemetry, voice, and gesture-aware control."""

    def __init__(self, fullscreen: bool = True, width: int = 1280, height: int = 720):
        self.fullscreen = fullscreen
        self.width = width
        self.height = height
        self.running = False
        self.state = "idle"
        self.status = "SYSTEM LOCKED"
        self.detail = "LAPTOP HUD // READY"
        self.audio = 0.0
        self._lock = threading.Lock()
        self._thread = None
        self._metrics = {
            "cpu": 0,
            "ram": 0,
            "battery": 0,
            "disk": 0,
            "network": "offline",
            "microphone": "ready",
            "camera": "ready",
            "gesture": "ready",
            "voice": "ready",
            "app": "desktop",
        }

    def set_state(self, state: str):
        with self._lock:
            self.state = state.lower()
            defaults = {
                "idle": ("SYSTEM LOCKED", "LAPTOP HUD // READY"),
                "listening": ("LISTENING", "VOICE INPUT // READY"),
                "thinking": ("PROCESSING", "NEURAL CORE // ANALYZING"),
                "speaking": ("JARVIS ACTIVE", "VOICE OUTPUT // ONLINE"),
                "error": ("SYSTEM ALERT", "ATTENTION REQUIRED"),
            }
            self.status, self.detail = defaults.get(self.state, ("SYSTEM", "LAPTOP HUD // READY"))

    def set_status(self, status: str, detail: Optional[str] = None):
        with self._lock:
            self.status = status.upper()
            if detail is not None:
                self.detail = detail.upper()

    def set_audio_level(self, value: float):
        with self._lock:
            self.audio = max(0.0, min(1.0, float(value)))

    def update_metrics(self, **metrics):
        with self._lock:
            self._metrics.update(metrics)

    def _read_metrics(self):
        battery = psutil.sensors_battery()
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        cpu = psutil.cpu_percent(interval=None)
        net = psutil.net_io_counters()
        network = "online" if net is not None else "offline"
        temp = None
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                for key, values in temps.items():
                    if values:
                        temp = values[0].current
                        break
        except Exception:
            temp = None

        metrics = {
            "cpu": int(cpu),
            "ram": int(ram.percent),
            "battery": int(battery.percent) if battery else 0,
            "disk": int((disk.used / disk.total) * 100),
            "network": network,
            "temperature": temp if temp is not None else "n/a",
            "microphone": self._metrics.get("microphone", "ready"),
            "camera": self._metrics.get("camera", "ready"),
            "gesture": self._metrics.get("gesture", "ready"),
            "voice": self._metrics.get("voice", "ready"),
            "app": self._metrics.get("app", "desktop"),
        }
        return metrics

    def start(self):
        if self.running:
            return
        self.running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        self.running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(1.0)

    def _draw_panel(self, surface, x, y, w, h, title, rows, color):
        pygame.draw.rect(surface, (*color, 24), (x, y, w, h), 1)
        pygame.draw.line(surface, (*color, 125), (x, y), (x + 28, y), 1)
        pygame.draw.line(surface, (*color, 125), (x, y), (x, y + 22), 1)
        pygame.draw.line(surface, (*color, 80), (x + w - 28, y + h), (x + w, y + h), 1)
        pygame.draw.line(surface, (*color, 80), (x + w, y + h - 22), (x + w, y + h), 1)

        font_title = pygame.font.SysFont("consolas", 11, bold=True)
        font_text = pygame.font.SysFont("consolas", 10)
        surface.blit(font_title.render(title, True, (*color, 220)), (x + 12, y + 9))

        y_offset = y + 32
        for key, value in rows:
            surface.blit(font_text.render(key, True, (130, 150, 175)), (x + 12, y_offset))
            val_text = font_text.render(value, True, (*color, 200))
            surface.blit(val_text, (x + w - val_text.get_width() - 12, y_offset))
            pygame.draw.line(surface, (*color, 25), (x + 12, y_offset + 16), (x + w - 12, y_offset + 16), 1)
            y_offset += 22

    def _draw_bar(self, surface, x, y, w, h, pct, color):
        pct = max(0, min(100, pct))
        border = pygame.Rect(x, y, w, h)
        pygame.draw.rect(surface, (30, 40, 52), border, border_radius=4)
        fill_w = int((w - 10) * (pct / 100.0))
        fill_rect = pygame.Rect(x + 5, y + 3, fill_w, h - 6)
        pygame.draw.rect(surface, (*color, 200), fill_rect, border_radius=4)
        pygame.draw.rect(surface, (*color, 80), border, 1, border_radius=4)

    def _draw_wave(self, surface, x, y, w, h, level, color):
        bars = 32
        gap = 2
        for i in range(bars):
            bar_h = 8 + (math.sin(i * 0.8 + time.time() * 3) * 0.5 + 0.5) * (h - 8)
            if i < bars * level:
                alpha = 180
                bar_color = (*color, alpha)
            else:
                alpha = 40
                bar_color = (90, 120, 150, alpha)
            pygame.draw.rect(surface, bar_color, (x + i * (w // bars + gap), y + (h - int(bar_h)) // 2, w // bars - 1, int(bar_h)), border_radius=2)

    def _render(self, screen, t):
        with self._lock:
            state = self.state
            audio = self.audio
            status = self.status
            detail = self.detail
            metrics = self._read_metrics()

        color = ORANGE if state in ("thinking", "speaking") else BLUE
        screen.fill(BG)

        cx = self.width // 2
        cy = int(self.height * 0.45)
        radius = min(self.width, self.height) * 0.23

        glow = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        pygame.draw.circle(glow, (*color, 14), (cx, cy), int(radius * 1.5))
        screen.blit(glow, (0, 0), special_flags=pygame.BLEND_ADD)

        pygame.draw.circle(screen, (*color, 35), (cx, cy), int(radius), 1)
        pygame.draw.circle(screen, (*color, 55), (cx, cy), int(radius * 0.8), 1)
        pygame.draw.circle(screen, (*color, 75), (cx, cy), int(radius * 0.56), 1)

        for i in range(48):
            a = t * 0.12 + i * math.tau / 48
            r1 = radius * 1.15
            r2 = radius * (1.15 + (0.04 if i % 4 == 0 else 0.015))
            p1 = (cx + math.cos(a) * r1, cy + math.sin(a) * r1)
            p2 = (cx + math.cos(a) * r2, cy + math.sin(a) * r2)
            pygame.draw.line(screen, (*color, 55 if i % 4 else 28), p1, p2, 1)

        ring_pct = min(1.0, (audio * 0.7) + 0.18 + abs(math.sin(t * 2.5)) * 0.18)
        arc_len = math.radians(290)
        rect = pygame.Rect(cx - radius, cy - radius, radius * 2, radius * 2)
        pygame.draw.arc(screen, (*color, 110), rect, math.radians(250), math.radians(250) + arc_len * ring_pct, 2)
        pygame.draw.arc(screen, (*color, 45), rect, math.radians(90), math.radians(450), 1)

        inner = radius * 0.52
        pulse = 1 + 0.12 * math.sin(t * 3.2)
        pygame.draw.circle(screen, (*color, 70), (cx, cy), int(inner * pulse), 1)
        pygame.draw.circle(screen, (*color, 180), (cx, cy), max(2, int(inner * 0.14)), 0)

        font_big = pygame.font.SysFont("consolas", 22, bold=True)
        font_mid = pygame.font.SysFont("consolas", 13)
        font_small = pygame.font.SysFont("consolas", 10)

        title = font_big.render(status, True, (*color, 230))
        subtitle = font_mid.render(detail, True, (*color, 160))
        screen.blit(title, title.get_rect(center=(cx, cy - 14)))
        screen.blit(subtitle, subtitle.get_rect(center=(cx, cy + 18)))

        voice_bar_x = cx - 220
        voice_bar_y = cy + 52
        self._draw_wave(screen, voice_bar_x, voice_bar_y, 440, 30, audio, color)
        screen.blit(font_small.render("VOICE LEVEL", True, (160, 175, 200)), (voice_bar_x, voice_bar_y - 18))

        left_panel = [
            ("CPU", f"{metrics['cpu']}%"),
            ("RAM", f"{metrics['ram']}%"),
            ("BAT", f"{metrics['battery']}%"),
            ("DISK", f"{metrics['disk']}%"),
        ]
        right_panel = [
            ("MIC", metrics['microphone'].upper()),
            ("CAM", metrics['camera'].upper()),
            ("GESTURE", metrics['gesture'].upper()),
            ("VOICE", metrics['voice'].upper()),
        ]
        self._draw_panel(screen, 24, self.height * 0.22, 200, 170, "LAPTOP", left_panel, BLUE)
        self._draw_panel(screen, self.width - 224, self.height * 0.22, 200, 170, "CONTROL", right_panel, BLUE)

        bottom_panel = [
            ("NETWORK", metrics['network'].upper()),
            ("TEMP", f"{metrics['temperature']}C" if isinstance(metrics['temperature'], (int, float)) else "N/A"),
            ("APP", metrics['app'].upper()),
            ("STATE", state.upper()),
        ]
        self._draw_panel(screen, 24, self.height - 140, self.width - 48, 110, "SYSTEM", bottom_panel, CYAN)

        bar_y = self.height - 28
        self._draw_bar(screen, 24, bar_y, self.width - 48, 8, metrics['cpu'], BLUE)
        self._draw_bar(screen, 24, bar_y + 16, self.width - 48, 6, metrics['ram'], GREEN)

        top_left = font_small.render("J.A.R.V.I.S // LAPTOP SYSTEM HUD", True, (*color, 170))
        top_right = font_small.render("VOICE + GESTURE ACTIVE", True, (*color, 170))
        screen.blit(top_left, (24, 18))
        screen.blit(top_right, (self.width - top_right.get_width() - 24, 18))

        bottom_left = font_small.render("LOCAL AI READY", True, (160, 185, 210))
        bottom_right = font_small.render(time.strftime("%H:%M:%S"), True, (*color, 180))
        screen.blit(bottom_left, (24, self.height - 28 - 30))
        screen.blit(bottom_right, (self.width - bottom_right.get_width() - 24, self.height - 28 - 30))

    def _loop(self):
        pygame.init()
        pygame.display.set_caption("JARVIS // Laptop HUD")
        flags = pygame.DOUBLEBUF | (pygame.FULLSCREEN if self.fullscreen else 0)
        if self.fullscreen:
            info = pygame.display.Info()
            self.width, self.height = info.current_w, info.current_h
        screen = pygame.display.set_mode((self.width, self.height), flags)
        clock = pygame.time.Clock()
        t0 = time.perf_counter()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_F11:
                        self.fullscreen = not self.fullscreen
                        flags = pygame.DOUBLEBUF | (pygame.FULLSCREEN if self.fullscreen else 0)
                        if self.fullscreen:
                            info = pygame.display.Info()
                            self.width, self.height = info.current_w, info.current_h
                        else:
                            self.width, self.height = 1280, 720
                        screen = pygame.display.set_mode((self.width, self.height), flags)

            self._render(screen, time.perf_counter() - t0)
            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()


if __name__ == "__main__":
    hud = JarvisHUD(fullscreen=False)
    hud.start()
    try:
        while hud.running:
            hud.update_metrics(
                cpu=psutil.cpu_percent(),
                ram=psutil.virtual_memory().percent,
                battery=int(psutil.sensors_battery().percent) if psutil.sensors_battery() else 0,
                app="system dashboard",
                gesture="ready",
                voice="ready",
                microphone="ready",
            )
            hud.set_audio_level(0.55 + 0.35 * abs(math.sin(time.time() * 2.1)))
            time.sleep(0.25)
    except KeyboardInterrupt:
        pass
    finally:
        hud.stop()
