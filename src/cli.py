import itertools
import signal
import sys
import threading
import time
from contextlib import contextmanager


class CancelToken:
    def __init__(self):
        self.cancelled = False
        self.lock = threading.Lock()
        self.handlers = []
        self.timeout = float("inf")

    def cancel(self, message: str = "Cancelled"):
        with self.lock:
            if not message:
                raise ValueError("message is required")

            # 初めのメッセージのみ保持する
            if not self.cancelled:
                self.cancelled = message
                for handler in self.handlers:
                    handler()

    @property
    def running(self):
        with self.lock:
            return not self.cancelled

    def get_cancel_message(self):
        with self.lock:
            if not self.cancelled:
                raise RuntimeError()
            return self.cancelled

    def handle_signal(self, *signums):
        """
        usage:

        import signal
        token = CancelToken()
        token.handle_signal(signal.SIGINT, signal.SIGTERM)
        """
        # signalは使い終わったら戻した方がいいらしい
        for signum in signums:
            signal.signal(signum, self.on_interrupt)

    def handle_keyboard_interrupt(self):
        """キーボードインタラプトを検知した時、トークンをキャンセルするハンドラを登録します"""
        self.handle_signal(signal.SIGINT)

    def on_interrupt(self, signum, frame):
        message = "Interrupted by signal {}".format(signum)
        self.cancel(message)

    def add_handler(self, handler):
        self.handlers.append(handler)

    def set_timeout(self, seconds):
        ...

    @property
    def is_timeouted(self):
        ...

    def block(self):
        while self.running:
            time.sleep(1)


class ProgressToken(CancelToken):
    def __init__(self):
        super().__init__()
        self.progress_message = ""

    def get_progress(self):
        with self.lock:
            return self.progress_message

    def update_progress(self, message):
        with self.lock:
            self.progress_message = message


class UIThread:
    def __init__(self, buf=None, delay=0.2):
        self.spinner = itertools.cycle(["-", "/", "|", "\\"])
        self.delay = delay
        self.running = False
        self.thread = None
        self.buf = buf or sys.stdout

    def spinner_task(self, token: ProgressToken):
        buf = self.buf
        old_msg = token.get_progress()
        buf.write(old_msg)
        buf.write(next(self.spinner))

        while token.running:
            new_msg = token.get_progress()
            if old_msg != new_msg:
                buf.write("\b" * (len(old_msg) + 1))
                buf.write(new_msg)
                old_msg = new_msg
            else:
                buf.write("\b")  # カーソルを一つ戻る

            buf.write(next(self.spinner))  # スピナーの次の状態を出力
            buf.flush()
            time.sleep(self.delay)

    def start(self, token: ProgressToken):
        if self.running:
            raise RuntimeError()
        self.running = True
        self.thread = threading.Thread(target=self.spinner_task, args=(token,))
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()
        self.buf.write("\b")  # スピナーをクリア

    def cancel(self):
        self.running = False

    @contextmanager
    def wait(self, cancel_token: ProgressToken = None):
        cancel_token = cancel_token or ProgressToken()
        # msg = cancel_token.get_progress()
        # self.buf.write(msg)
        # self.buf.flush()

        cancel_token.add_handler(self.cancel)
        self.start(cancel_token)

        try:
            yield cancel_token
        finally:
            cancel_token.cancel()
            self.stop()
            time.sleep(self.delay)

            self.buf.write("\n")
            self.buf.flush()
