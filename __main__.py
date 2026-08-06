import platform
import sys
import time
from dataclasses import dataclass

from me import generate_header


@dataclass
class Settings:
    duration: float
    rate: float
    randomize: bool
    randomize_min: float
    os: str


questions = {
    "os": "Nie wykryto systemu. Wpisz go (tylko Windows i Linux):\n>\t",
    "duration": "Jak długo Auto Clicker ma działać? (w sekundach; domyślnie: 2; 0 = bez limitu):\n>\t",
    "rate": "Ile CPS? (domyślnie: 1):\n>\t",
    "randomize_rate": "Czy odstęp między kliknięciami ma być losowy? (domyślnie: Tak):\n>\t",
    "randomize_rate_min": "Minimalny odstęp między kliknięciami (w sekundach; domyślnie: 0.1):\n>\t",
    "is_good?": "Wszystko się zgadza? ([T]/n) (domyślnie: Tak):\n>\t",
}

invalid = {
    "os": "Nieobsługiwany system!",
    "duration": "Czas trwania musi być poprawną liczbą >= 0.",
    "rate": "Szybkość musi być poprawną liczbą >= 0.",
    "randomize_rate_min": "Minimalny czas losowania musi być poprawną liczbą > 0.",
    "impossible_fluctuation": "Brak możliwości losowania przy tych wartościach!",
    "import": "Tego pliku nie należy importować.",
}

info = {
    "running": "Auto Clicker działa... Wciśnij 'Ctrl+C' aby wymusić zatrzymanie",
    "os": "System",
    "duration": "Czas działania",
    "rate": "Szybkość klikania",
    "randomize_rate": "Losowy czas?",
    "randomize_rate_min": "Czas minimalny",
    "indefinite": "Bez limitu",
    "end": "Koniec klikania",
    "stopping": "Zatrzymywanie...",
    "header": generate_header() + "\n",
}
if __name__ != "__main__":
    raise ImportError(invalid["import"])

true_values = {"true", "t", "y", "yes", "1", 1, "on", "", " "}
supported_os = {"windows", "win32", "windows nt", "linux", "linuxbsd"}


def is_true(input: str) -> bool:
    return input.lower() in true_values


def is_supported_os(input: str):
    return input.lower() in supported_os


def is_valid_number(input: str) -> bool:
    try:
        return float(input)

    except ValueError:
        return False


def ask_number(question, default, error, *, minimum=None, zero_means=None):
    while True:
        value = input(question).strip()

        if not value:
            return default

        try:
            value = float(value)
        except ValueError:
            print(error)
            continue

        if zero_means is not None and value == 0:
            return zero_means

        if minimum is not None and value < minimum:
            print(error)
            continue

        return value


duration = 0
rate = 0

rand_rate = False
rand_dur_min = 0.1

current_os = ""


def get_settings() -> Settings:

    def ask_os() -> str:
        os = platform.system()
        if not is_supported_os(os):
            in_os = input(questions["os"])
            if is_supported_os(in_os):
                os = in_os
            else:
                return ask_os()

        return os

    current_os = ask_os()

    in_duration = ask_number(questions["duration"], default=2, error=invalid["duration"], minimum=0, zero_means=-1)

    in_rate = ask_number(
        questions["rate"], default=1, error=invalid["rate"], minimum=sys.float_info.epsilon, zero_means=0
    )

    def ask_randomize_rate() -> bool:
        in_str = input(questions["randomize_rate"])
        return bool(is_true(in_str) or in_str == "")

    in_randomize_rate = ask_randomize_rate()
    in_randomize_rate_min = 0
    if in_randomize_rate:
        in_randomize_rate_min = ask_number(
            questions["randomize_rate_min"],
            default=0.1,
            error=invalid["randomize_rate_min"],
            minimum=sys.float_info.epsilon,
        )

    def ask_is_good() -> None:
        print("\n")
        print(f"{info['os']} {current_os}")

        if in_duration != -1:
            print(f"{info['duration']} {in_duration}")
        else:
            print(f"{info['duration']} {info['indefinite']}")

        print(f"{info['rate']} {in_rate}")
        print(f"{info['randomize_rate']} {in_randomize_rate}")
        if in_randomize_rate:
            print(f"{info['randomize_rate_min']} {in_randomize_rate_min}")

        in_bool = input(questions["is_good?"])
        if not is_true(in_bool) and in_bool != "":
            return get_settings()

    ask_is_good()

    return Settings(
        duration=in_duration,
        rate=in_rate,
        randomize=in_randomize_rate,
        randomize_min=in_randomize_rate_min,
        os=current_os.lower(),
    )


def countdown(seconds: int) -> None:
    for i in range(seconds, 0, -1):
        print(f"In {i}...\r", end="", flush=True)
        time.sleep(1)


def steady_click(cfg: Settings) -> None:
    avg_sleep_rate = 1 / cfg.rate

    c_dur_acc = 0
    c_dur_maxacc = 0
    if duration != -1:
        c_dur_maxacc = cfg.duration * cfg.rate

    countdown(5)
    print(info["running"])

    while c_dur_acc < c_dur_maxacc or cfg.duration == -1:
        time.sleep(avg_sleep_rate)
        click()

        if cfg.duration != -1:
            c_dur_acc += 1


def generate_batch(batch_size, min_sleep, max_sleep, target_sleep):
    import numpy as np

    holds = np.random.uniform(0.002, 0.015, size=batch_size)

    target = batch_size * target_sleep - holds.sum()
    target = max(0, target)

    sleeps = np.random.uniform(min_sleep, max_sleep, size=batch_size)

    jump_mask = np.random.rand(batch_size) < 0.04
    sleeps = np.where(jump_mask, sleeps + np.random.uniform(0.02, 0.06, size=batch_size), sleeps)

    sleeps = np.clip(sleeps, min_sleep, max_sleep)

    if sleeps.sum() > 0 and target > 0:
        sleeps *= target / sleeps.sum()
    else:
        sleeps.fill(max(0, target_sleep - holds.mean()))

    return sleeps, holds


def fluctuating_click(cfg: Settings) -> None:

    min_sleep_rate = float(cfg.randomize_min)
    target_sleep_rate = float(1 / cfg.rate)
    max_sleep_rate = (2 * target_sleep_rate) - min_sleep_rate

    if max_sleep_rate < min_sleep_rate:
        raise ValueError(invalid["impossible_fluctuation"])

    c_dur_acc = 0

    if cfg.duration != -1:
        batch_size = int(cfg.duration * cfg.rate)
        if batch_size <= 0:
            return
        target_sleep = float(cfg.duration) / batch_size
    else:
        batch_size = 1000
        target_sleep = target_sleep_rate

    countdown(5)
    print(info["running"])

    while True:
        sleeps, holds = generate_batch(
            batch_size,
            min_sleep_rate,
            max_sleep_rate,
            target_sleep,
        )

        for sleep_time, hold_time in zip(sleeps, holds):
            time.sleep(float(sleep_time))
            click.press()
            time.sleep(float(hold_time))
            click.release()
            c_dur_acc += 1

        if cfg.duration != -1:
            break


print(info["header"])

try:
    cfg = get_settings()

    if cfg.rate == 0:
        raise ValueError(invalid["rate"])

    match cfg.os:
        case "linux":
            from click_platform.Linux import Click

        case "windows":
            from click_platform.Windows import Click

        case _:
            raise OSError(f"{invalid['os']} {cfg.os}")

    click = Click()
    if not cfg.randomize:
        steady_click(cfg)
    else:
        fluctuating_click(cfg)

    print(info["end"])

except KeyboardInterrupt:
    print(f"\n{info['stopping']}")
